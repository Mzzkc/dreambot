import random


def zalgo_text(text, intensity='medium'):
    """Generate zalgo text with comprehensive coverage"""
    zalgo_up = [
        '\u030d', '\u030e', '\u0304', '\u0305', '\u033f', '\u0311', '\u0306', '\u0310', '\u0352',
        '\u0357', '\u0351', '\u0307', '\u0308', '\u030a', '\u0342', '\u0343', '\u0344', '\u034a',
        '\u034b', '\u034c', '\u0303', '\u0302', '\u030c', '\u0350', '\u0300', '\u030b', '\u030f',
        '\u0312', '\u0313', '\u0314', '\u033d', '\u0309', '\u0363'
    ]

    zalgo_mid = [
        '\u0315', '\u031b', '\u0340', '\u0341', '\u0358', '\u0321', '\u0322', '\u0327', '\u0328',
        '\u0334', '\u0335', '\u0336', '\u034f', '\u035c', '\u035d', '\u035e', '\u035f', '\u0360'
    ]

    zalgo_down = [
        '\u0316', '\u0317', '\u0318', '\u0319', '\u031c', '\u031d', '\u031e', '\u031f', '\u0320',
        '\u0324', '\u0325', '\u0326', '\u0329', '\u032a', '\u032b', '\u032c', '\u032d', '\u032e',
        '\u032f', '\u0330', '\u0331', '\u0332', '\u0333', '\u0339', '\u033a', '\u033b', '\u033c',
        '\u0345', '\u0347', '\u0348', '\u0349', '\u034d', '\u034e', '\u0353', '\u0354', '\u0355'
    ]

    intensity_map = {
        'low': (0, 2),
        'medium': (1, 3),
        'high': (2, 4),
        'extreme': (3, 6)
    }

    min_chars, max_chars = intensity_map.get(intensity, (1, 3))

    result = ""
    for char in text:
        result += char

        for _ in range(random.randint(min_chars, max_chars)):
            result += random.choice(zalgo_up)

        if random.random() < 0.3:
            for _ in range(random.randint(0, max_chars - 1)):
                result += random.choice(zalgo_mid)

        for _ in range(random.randint(min_chars, max_chars)):
            result += random.choice(zalgo_down)

    return result


def zalgo_embed(description=None, title=None, color=None, **kwargs):
    """
    Create an embed with zalgo-transformed description.

    Args:
        description: Main description text (will be zalgo'd with 'low' intensity)
        title: Title text (not zalgo'd for readability)
        color: Embed color
        **kwargs: Any other discord.Embed parameters

    Returns:
        discord.Embed with zalgo-transformed description
    """
    import discord

    embed = discord.Embed(color=color or discord.Color.dark_purple(), **kwargs)

    if title:
        embed.title = title

    if description:
        # Apply low intensity for readability in embeds
        zalgo_desc = zalgo_text(description, intensity='low')
        embed.description = zalgo_desc

    return embed