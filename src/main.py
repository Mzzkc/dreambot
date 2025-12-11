import os
import asyncio
import random
import logging
from keep_alive import keep_alive
from bot import create_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limit handling configuration
MAX_RETRIES = 10
BASE_DELAY = 30  # Start with 30 second delay for Cloudflare-level blocks
MAX_DELAY = 900  # Cap at 15 minutes
JITTER_RANGE = 0.5  # ±50% jitter to prevent thundering herd

# Slumber mode configuration (when all retries exhausted)
SLUMBER_DURATION_HOURS = 2  # How long to sleep before fresh retry cycle
MAX_SLUMBER_CYCLES = 12  # Max slumber cycles before truly giving up (24 hours total)


async def attempt_connection_cycle(token):
    """
    Attempt to connect to Discord with exponential backoff.

    Returns:
        bool: True if connected successfully, False if all retries exhausted due to 429
    Raises:
        Exception: For non-429 errors that should not trigger slumber
    """
    import discord

    bot = create_bot()
    retry_count = 0

    while retry_count < MAX_RETRIES:
        try:
            logger.info(f"Attempting to connect to Discord (attempt {retry_count + 1}/{MAX_RETRIES})...")
            await bot.start(token)
            # If we get here, bot.start() exited cleanly (unlikely during normal operation)
            return True

        except discord.errors.HTTPException as e:
            if e.status == 429:
                retry_count += 1

                # Calculate delay with exponential backoff
                delay = min(BASE_DELAY * (2 ** (retry_count - 1)), MAX_DELAY)

                # Add jitter (±50%) to prevent thundering herd
                jitter = delay * random.uniform(-JITTER_RANGE, JITTER_RANGE)
                actual_delay = delay + jitter

                # Check if Discord sent a Retry-After header
                retry_after = getattr(e, 'retry_after', None)
                if retry_after and retry_after > actual_delay:
                    actual_delay = retry_after + random.uniform(1, 5)

                logger.warning(
                    f"Rate limited (429). Attempt {retry_count}/{MAX_RETRIES}. "
                    f"Waiting {actual_delay:.1f}s before retry..."
                )

                await asyncio.sleep(actual_delay)

                # Recreate bot instance to clear any stale state
                bot = create_bot()

            else:
                # Non-rate-limit HTTP error - log and re-raise
                logger.error(f"HTTP error {e.status}: {e.text}")
                raise

        except discord.errors.LoginFailure as e:
            logger.error(f"Login failed - check DISCORD_TOKEN: {e}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during bot startup: {type(e).__name__}: {e}")
            raise

    # All retries exhausted due to 429
    return False


async def start_bot_with_backoff():
    """
    Start the bot with exponential backoff and slumber mode for rate limit handling.

    Discord's Cloudflare protection can issue 429s at the IP/token level,
    especially during deployments when multiple instances try to connect.

    Strategy:
    1. Try to connect with exponential backoff (up to MAX_RETRIES)
    2. If all retries exhausted, enter "slumber mode" for SLUMBER_DURATION_HOURS
    3. After slumber, start a fresh connection cycle
    4. Repeat up to MAX_SLUMBER_CYCLES before truly giving up

    This allows the bot to wait out even extended Cloudflare blocks (up to 24 hours).
    """
    token = os.getenv('DISCORD_TOKEN')

    if not token:
        logger.error("DISCORD_TOKEN environment variable not set!")
        return

    slumber_count = 0

    while slumber_count <= MAX_SLUMBER_CYCLES:
        # Attempt a full connection cycle
        connected = await attempt_connection_cycle(token)

        if connected:
            # Successfully connected (or bot.start() exited cleanly)
            return

        # Connection cycle exhausted all retries due to 429
        slumber_count += 1

        if slumber_count > MAX_SLUMBER_CYCLES:
            break

        # Enter slumber mode
        slumber_seconds = SLUMBER_DURATION_HOURS * 3600
        # Add some jitter to slumber duration (±10%)
        jitter = slumber_seconds * random.uniform(-0.1, 0.1)
        actual_slumber = slumber_seconds + jitter

        logger.warning(
            f"All {MAX_RETRIES} connection attempts failed. "
            f"Entering slumber mode (cycle {slumber_count}/{MAX_SLUMBER_CYCLES}). "
            f"Sleeping for {SLUMBER_DURATION_HOURS} hours before retry..."
        )

        await asyncio.sleep(actual_slumber)

        logger.info(f"Waking from slumber. Starting fresh connection cycle...")

    # Exhausted all slumber cycles
    total_wait_hours = MAX_SLUMBER_CYCLES * SLUMBER_DURATION_HOURS
    logger.error(
        f"Failed to connect after {MAX_SLUMBER_CYCLES} slumber cycles "
        f"(~{total_wait_hours} hours). Giving up."
    )
    raise RuntimeError(
        f"Could not connect to Discord after {MAX_SLUMBER_CYCLES} slumber cycles"
    )


async def main():
    """Main entry point"""
    keep_alive()
    await start_bot_with_backoff()


if __name__ == "__main__":
    asyncio.run(main())