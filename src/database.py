import os
import json
import logging
from supabase import create_client, Client

# Set up logging
logger = logging.getLogger(__name__)

class BotDatabase:
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')

        if url and key:
            try:
                self.supabase: Client = create_client(url, key)
                self.init_tables()
                logger.info("[Database] Initialized with Supabase connection")
            except Exception as e:
                logger.error(f"[Database] Failed to initialize Supabase: {type(e).__name__}: {e}")
                logger.warning("[Database] Falling back to JSON storage")
                self.supabase = None
                self.use_json = True
        else:
            logger.warning("[Database] No Supabase credentials found, using JSON fallback")
            self.supabase = None
            # Fallback to JSON files
            self.use_json = True
    
    def init_tables(self):
        """Tables must be created via Supabase dashboard first"""
        # We'll provide SQL commands for this
        pass
    
    def load_reaction_roles(self):
        """Load reaction roles from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('reaction_roles.json', 'r') as f:
                    data = json.load(f)
                    logger.info(f"[Database] load_reaction_roles: Success ({len(data)} items from JSON)")
                    return data
            except FileNotFoundError:
                logger.info("[Database] load_reaction_roles: No JSON file found, returning empty dict")
                return {}
            except Exception as e:
                logger.error(f"[Database] load_reaction_roles: JSON read failed: {type(e).__name__}: {e}")
                return {}

        try:
            response = self.supabase.table('reaction_roles').select("*").execute()
            data = {item['message_id']: item['data'] for item in response.data}
            logger.info(f"[Database] load_reaction_roles: Success ({len(data)} items from Supabase)")
            return data
        except Exception as e:
            logger.error(f"[Database] load_reaction_roles: Supabase query failed: {type(e).__name__}: {e}")
            return {}
    
    def save_reaction_roles(self, data):
        """Save reaction roles to Supabase or JSON"""
        if not self.supabase:
            try:
                with open('reaction_roles.json', 'w') as f:
                    json.dump(data, f)
                logger.info(f"[Database] save_reaction_roles: Success ({len(data)} items to JSON)")
            except Exception as e:
                logger.error(f"[Database] save_reaction_roles: JSON write failed: {type(e).__name__}: {e}")
            return

        try:
            # Clear existing
            self.supabase.table('reaction_roles').delete().neq('message_id', '0').execute()

            # Insert new data
            for message_id, msg_data in data.items():
                self.supabase.table('reaction_roles').upsert({
                    'message_id': message_id,
                    'data': msg_data
                }).execute()
            logger.info(f"[Database] save_reaction_roles: Success ({len(data)} items to Supabase)")
        except Exception as e:
            logger.warning(f"[Database] save_reaction_roles: Supabase error, falling back to JSON: {type(e).__name__}: {e}")
            try:
                with open('reaction_roles.json', 'w') as f:
                    json.dump(data, f)
                logger.info(f"[Database] save_reaction_roles: JSON fallback successful ({len(data)} items)")
            except Exception as json_e:
                logger.error(f"[Database] save_reaction_roles: JSON fallback failed: {type(json_e).__name__}: {json_e}")
    
    def load_warnings(self):
        """Load warnings from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('warnings.json', 'r') as f:
                    data = json.load(f)
                    # Count total warnings across all guilds/users
                    count = sum(len(users) for users in data.values())
                    logger.info(f"[Database] load_warnings: Success ({count} users from JSON)")
                    return data
            except FileNotFoundError:
                logger.info("[Database] load_warnings: No JSON file found, returning empty dict")
                return {}
            except Exception as e:
                logger.error(f"[Database] load_warnings: JSON read failed: {type(e).__name__}: {e}")
                return {}

        try:
            response = self.supabase.table('warnings').select("*").execute()
            warnings_dict = {}
            for item in response.data:
                guild_id = item['guild_id']
                user_id = item['user_id']
                if guild_id not in warnings_dict:
                    warnings_dict[guild_id] = {}
                warnings_dict[guild_id][user_id] = item['warnings']
            count = sum(len(users) for users in warnings_dict.values())
            logger.info(f"[Database] load_warnings: Success ({count} users from Supabase)")
            return warnings_dict
        except Exception as e:
            logger.error(f"[Database] load_warnings: Supabase query failed: {type(e).__name__}: {e}")
            return {}
    
    def save_warnings(self, data):
        """Save warnings to Supabase or JSON"""
        count = sum(len(users) for users in data.values())

        if not self.supabase:
            try:
                with open('warnings.json', 'w') as f:
                    json.dump(data, f)
                logger.info(f"[Database] save_warnings: Success ({count} users to JSON)")
            except Exception as e:
                logger.error(f"[Database] save_warnings: JSON write failed: {type(e).__name__}: {e}")
            return

        try:
            # Clear existing
            self.supabase.table('warnings').delete().neq('guild_id', '0').execute()

            # Insert new data
            for guild_id, guild_warnings in data.items():
                for user_id, user_warnings in guild_warnings.items():
                    self.supabase.table('warnings').upsert({
                        'guild_id': guild_id,
                        'user_id': user_id,
                        'warnings': user_warnings
                    }).execute()
            logger.info(f"[Database] save_warnings: Success ({count} users to Supabase)")
        except Exception as e:
            logger.warning(f"[Database] save_warnings: Supabase error, falling back to JSON: {type(e).__name__}: {e}")
            try:
                with open('warnings.json', 'w') as f:
                    json.dump(data, f)
                logger.info(f"[Database] save_warnings: JSON fallback successful ({count} users)")
            except Exception as json_e:
                logger.error(f"[Database] save_warnings: JSON fallback failed: {type(json_e).__name__}: {json_e}")

    def load_suggestions(self):
        """Load suggestions from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('suggestions.json', 'r') as f:
                    data = json.load(f)
                    logger.info(f"[Database] load_suggestions: Success ({len(data)} items from JSON)")
                    return data
            except FileNotFoundError:
                logger.info("[Database] load_suggestions: No JSON file found, returning empty dict")
                return {}
            except Exception as e:
                logger.error(f"[Database] load_suggestions: JSON read failed: {type(e).__name__}: {e}")
                return {}

        try:
            response = self.supabase.table('suggestions').select("*").execute()
            data = {item['message_id']: item['data'] for item in response.data}
            logger.info(f"[Database] load_suggestions: Success ({len(data)} items from Supabase)")
            return data
        except Exception as e:
            logger.error(f"[Database] load_suggestions: Supabase query failed: {type(e).__name__}: {e}")
            return {}

    def save_suggestions(self, data):
        """Save suggestions to Supabase or JSON"""
        if not self.supabase:
            try:
                with open('suggestions.json', 'w') as f:
                    json.dump(data, f)
                logger.info(f"[Database] save_suggestions: Success ({len(data)} items to JSON)")
            except Exception as e:
                logger.error(f"[Database] save_suggestions: JSON write failed: {type(e).__name__}: {e}")
            return

        try:
            # Clear existing
            self.supabase.table('suggestions').delete().neq('message_id', '0').execute()

            # Insert new data
            for message_id, suggestion_data in data.items():
                self.supabase.table('suggestions').upsert({
                    'message_id': message_id,
                    'data': suggestion_data
                }).execute()
            logger.info(f"[Database] save_suggestions: Success ({len(data)} items to Supabase)")
        except Exception as e:
            logger.warning(f"[Database] save_suggestions: Supabase error, falling back to JSON: {type(e).__name__}: {e}")
            try:
                with open('suggestions.json', 'w') as f:
                    json.dump(data, f)
                logger.info(f"[Database] save_suggestions: JSON fallback successful ({len(data)} items)")
            except Exception as json_e:
                logger.error(f"[Database] save_suggestions: JSON fallback failed: {type(json_e).__name__}: {json_e}")

    def load_whisper_usage(self):
        """Load whisper usage statistics from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('whisper_usage.json', 'r') as f:
                    data = json.load(f)
                    logger.info(f"[Database] load_whisper_usage: Success ({len(data)} whispers from JSON)")
                    return data
            except FileNotFoundError:
                logger.info("[Database] load_whisper_usage: No JSON file found, returning empty dict")
                return {}
            except Exception as e:
                logger.error(f"[Database] load_whisper_usage: JSON read failed: {type(e).__name__}: {e}")
                return {}

        try:
            response = self.supabase.table('whisper_usage').select("*").execute()
            # Return dict keyed by whisper_id
            data = {item['whisper_id']: {
                'text': item['whisper_text'],
                'usage_count': item['usage_count'],
                'last_used': item['last_used']
            } for item in response.data}
            logger.info(f"[Database] load_whisper_usage: Success ({len(data)} whispers from Supabase)")
            return data
        except Exception as e:
            logger.error(f"[Database] load_whisper_usage: Supabase query failed: {type(e).__name__}: {e}")
            return {}

    def save_whisper_usage(self, data):
        """Save whisper usage statistics to Supabase or JSON"""
        if not self.supabase:
            try:
                with open('whisper_usage.json', 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"[Database] save_whisper_usage: Success ({len(data)} whispers to JSON)")
            except Exception as e:
                logger.error(f"[Database] save_whisper_usage: JSON write failed: {type(e).__name__}: {e}")
            return

        try:
            # Clear existing
            self.supabase.table('whisper_usage').delete().neq('whisper_id', '').execute()

            # Insert new data
            for whisper_id, stats in data.items():
                self.supabase.table('whisper_usage').upsert({
                    'whisper_id': whisper_id,
                    'whisper_text': stats['text'],
                    'usage_count': stats['usage_count'],
                    'last_used': stats['last_used']
                }).execute()
            logger.info(f"[Database] save_whisper_usage: Success ({len(data)} whispers to Supabase)")
        except Exception as e:
            logger.warning(f"[Database] save_whisper_usage: Supabase error, falling back to JSON: {type(e).__name__}: {e}")
            try:
                with open('whisper_usage.json', 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"[Database] save_whisper_usage: JSON fallback successful ({len(data)} whispers)")
            except Exception as json_e:
                logger.error(f"[Database] save_whisper_usage: JSON fallback failed: {type(json_e).__name__}: {json_e}")

    def increment_whisper_usage(self, whisper_id, whisper_text):
        """Increment usage count for a whisper (ID-based)"""
        from datetime import datetime, timezone

        try:
            usage_data = self.load_whisper_usage()

            if whisper_id not in usage_data:
                usage_data[whisper_id] = {'text': whisper_text, 'usage_count': 0, 'last_used': None}
                logger.debug(f"[Database] increment_whisper_usage: New whisper '{whisper_id}'")

            # Update both usage AND text (in case text was edited in constants.py)
            usage_data[whisper_id]['text'] = whisper_text
            usage_data[whisper_id]['usage_count'] += 1
            usage_data[whisper_id]['last_used'] = datetime.now(timezone.utc).isoformat()
            new_count = usage_data[whisper_id]['usage_count']

            self.save_whisper_usage(usage_data)
            logger.debug(f"[Database] increment_whisper_usage: '{whisper_id}' now at {new_count} uses")
            return new_count
        except Exception as e:
            logger.error(f"[Database] increment_whisper_usage: Failed for '{whisper_id}': {type(e).__name__}: {e}")
            return 1  # Return 1 as fallback to indicate it was used once

    def load_8ball_usage(self):
        """Load 8-ball response usage statistics from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('8ball_usage.json', 'r') as f:
                    data = json.load(f)
                    logger.info(f"[Database] load_8ball_usage: Success ({len(data)} responses from JSON)")
                    return data
            except FileNotFoundError:
                logger.info("[Database] load_8ball_usage: No JSON file found, returning empty dict")
                return {}
            except Exception as e:
                logger.error(f"[Database] load_8ball_usage: JSON read failed: {type(e).__name__}: {e}")
                return {}

        try:
            response = self.supabase.table('response_8ball_usage').select("*").execute()
            # Return dict keyed by response_id
            data = {item['response_id']: {
                'text': item['response_text'],
                'usage_count': item['usage_count'],
                'last_used': item['last_used']
            } for item in response.data}
            logger.info(f"[Database] load_8ball_usage: Success ({len(data)} responses from Supabase)")
            return data
        except Exception as e:
            logger.error(f"[Database] load_8ball_usage: Supabase query failed: {type(e).__name__}: {e}")
            return {}

    def save_8ball_usage(self, data):
        """Save 8-ball response usage statistics to Supabase or JSON"""
        if not self.supabase:
            try:
                with open('8ball_usage.json', 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"[Database] save_8ball_usage: Success ({len(data)} responses to JSON)")
            except Exception as e:
                logger.error(f"[Database] save_8ball_usage: JSON write failed: {type(e).__name__}: {e}")
            return

        try:
            # Clear existing
            self.supabase.table('response_8ball_usage').delete().neq('response_id', '').execute()

            # Insert new data
            for response_id, stats in data.items():
                self.supabase.table('response_8ball_usage').upsert({
                    'response_id': response_id,
                    'response_text': stats['text'],
                    'usage_count': stats['usage_count'],
                    'last_used': stats['last_used']
                }).execute()
            logger.info(f"[Database] save_8ball_usage: Success ({len(data)} responses to Supabase)")
        except Exception as e:
            logger.warning(f"[Database] save_8ball_usage: Supabase error, falling back to JSON: {type(e).__name__}: {e}")
            try:
                with open('8ball_usage.json', 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"[Database] save_8ball_usage: JSON fallback successful ({len(data)} responses)")
            except Exception as json_e:
                logger.error(f"[Database] save_8ball_usage: JSON fallback failed: {type(json_e).__name__}: {json_e}")

    def increment_8ball_usage(self, response_id, response_text):
        """Increment usage count for an 8-ball response (ID-based)"""
        from datetime import datetime, timezone

        try:
            usage_data = self.load_8ball_usage()

            if response_id not in usage_data:
                usage_data[response_id] = {'text': response_text, 'usage_count': 0, 'last_used': None}
                logger.debug(f"[Database] increment_8ball_usage: New response '{response_id}'")

            # Update both usage AND text (in case text was edited in constants.py)
            usage_data[response_id]['text'] = response_text
            usage_data[response_id]['usage_count'] += 1
            usage_data[response_id]['last_used'] = datetime.now(timezone.utc).isoformat()
            new_count = usage_data[response_id]['usage_count']

            self.save_8ball_usage(usage_data)
            logger.debug(f"[Database] increment_8ball_usage: '{response_id}' now at {new_count} uses")
            return new_count
        except Exception as e:
            logger.error(f"[Database] increment_8ball_usage: Failed for '{response_id}': {type(e).__name__}: {e}")
            return 1  # Return 1 as fallback to indicate it was used once

    def load_vague_usage(self):
        """Load vague statement usage statistics from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('vague_usage.json', 'r') as f:
                    data = json.load(f)
                    logger.info(f"[Database] load_vague_usage: Success ({len(data)} statements from JSON)")
                    return data
            except FileNotFoundError:
                logger.info("[Database] load_vague_usage: No JSON file found, returning empty dict")
                return {}
            except Exception as e:
                logger.error(f"[Database] load_vague_usage: JSON read failed: {type(e).__name__}: {e}")
                return {}

        try:
            response = self.supabase.table('response_vague_usage').select("*").execute()
            # Return dict keyed by statement_id
            data = {item['statement_id']: {
                'text': item['statement_text'],
                'usage_count': item['usage_count'],
                'last_used': item['last_used']
            } for item in response.data}
            logger.info(f"[Database] load_vague_usage: Success ({len(data)} statements from Supabase)")
            return data
        except Exception as e:
            logger.error(f"[Database] load_vague_usage: Supabase query failed: {type(e).__name__}: {e}")
            return {}

    def save_vague_usage(self, data):
        """Save vague statement usage statistics to Supabase or JSON"""
        if not self.supabase:
            try:
                with open('vague_usage.json', 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"[Database] save_vague_usage: Success ({len(data)} statements to JSON)")
            except Exception as e:
                logger.error(f"[Database] save_vague_usage: JSON write failed: {type(e).__name__}: {e}")
            return

        try:
            # Clear existing
            self.supabase.table('response_vague_usage').delete().neq('statement_id', '').execute()

            # Insert new data
            for statement_id, stats in data.items():
                self.supabase.table('response_vague_usage').upsert({
                    'statement_id': statement_id,
                    'statement_text': stats['text'],
                    'usage_count': stats['usage_count'],
                    'last_used': stats['last_used']
                }).execute()
            logger.info(f"[Database] save_vague_usage: Success ({len(data)} statements to Supabase)")
        except Exception as e:
            logger.warning(f"[Database] save_vague_usage: Supabase error, falling back to JSON: {type(e).__name__}: {e}")
            try:
                with open('vague_usage.json', 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"[Database] save_vague_usage: JSON fallback successful ({len(data)} statements)")
            except Exception as json_e:
                logger.error(f"[Database] save_vague_usage: JSON fallback failed: {type(json_e).__name__}: {json_e}")

    def increment_vague_usage(self, statement_id, statement_text):
        """Increment usage count for a vague statement (ID-based)"""
        from datetime import datetime, timezone

        try:
            usage_data = self.load_vague_usage()

            if statement_id not in usage_data:
                usage_data[statement_id] = {'text': statement_text, 'usage_count': 0, 'last_used': None}
                logger.debug(f"[Database] increment_vague_usage: New statement '{statement_id}'")

            # Update both usage AND text (in case text was edited in constants.py)
            usage_data[statement_id]['text'] = statement_text
            usage_data[statement_id]['usage_count'] += 1
            usage_data[statement_id]['last_used'] = datetime.now(timezone.utc).isoformat()
            new_count = usage_data[statement_id]['usage_count']

            self.save_vague_usage(usage_data)
            logger.debug(f"[Database] increment_vague_usage: '{statement_id}' now at {new_count} uses")
            return new_count
        except Exception as e:
            logger.error(f"[Database] increment_vague_usage: Failed for '{statement_id}': {type(e).__name__}: {e}")
            return 1  # Return 1 as fallback to indicate it was used once

    # =========================================================================
    # GENERIC INTENT POOL FUNCTIONS (Phase 1)
    # =========================================================================

    def load_pool_usage(self, pool_name):
        """
        Generic pool usage loader for any response pool.

        Args:
            pool_name (str): Pool identifier (e.g., 'greeting', 'kebab')

        Returns:
            dict: Usage data keyed by response_id
        """
        json_file = f'{pool_name}_usage.json'
        table_name = f'response_{pool_name}_usage'

        if not self.supabase:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    logger.info(f"[Database] load_pool_usage({pool_name}): Success ({len(data)} items from JSON)")
                    return data
            except FileNotFoundError:
                logger.info(f"[Database] load_pool_usage({pool_name}): No JSON file found, returning empty dict")
                return {}
            except Exception as e:
                logger.error(f"[Database] load_pool_usage({pool_name}): JSON read failed: {type(e).__name__}: {e}")
                return {}

        try:
            response = self.supabase.table(table_name).select("*").execute()
            # Log raw response for debugging
            if not response.data:
                logger.warning(f"[Database] load_pool_usage({pool_name}): Table '{table_name}' returned empty (count={response.count})")
            data = {item['response_id']: {
                'text': item['response_text'],
                'usage_count': item['usage_count'],
                'last_used': item['last_used']
            } for item in response.data}
            logger.info(f"[Database] load_pool_usage({pool_name}): Success ({len(data)} items from Supabase)")
            return data
        except Exception as e:
            logger.error(f"[Database] load_pool_usage({pool_name}): Supabase query failed: {type(e).__name__}: {e}")
            return {}

    def save_pool_usage(self, pool_name, data):
        """
        Generic pool usage saver for any response pool.

        Args:
            pool_name (str): Pool identifier
            data (dict): Usage data to save
        """
        json_file = f'{pool_name}_usage.json'
        table_name = f'response_{pool_name}_usage'

        if not self.supabase:
            try:
                with open(json_file, 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"[Database] save_pool_usage({pool_name}): Success ({len(data)} items to JSON)")
            except Exception as e:
                logger.error(f"[Database] save_pool_usage({pool_name}): JSON write failed: {type(e).__name__}: {e}")
            return

        try:
            # Clear existing
            delete_response = self.supabase.table(table_name).delete().neq('response_id', '').execute()
            logger.debug(f"[Database] save_pool_usage({pool_name}): Deleted {len(delete_response.data) if delete_response.data else 0} rows")

            # Insert new data
            for response_id, stats in data.items():
                upsert_response = self.supabase.table(table_name).upsert({
                    'response_id': response_id,
                    'response_text': stats['text'],
                    'usage_count': stats['usage_count'],
                    'last_used': stats['last_used']
                }).execute()
                # Check if upsert actually worked
                if not upsert_response.data:
                    logger.warning(f"[Database] save_pool_usage({pool_name}): Upsert for '{response_id}' returned no data - may have failed silently")
            logger.info(f"[Database] save_pool_usage({pool_name}): Success ({len(data)} items to Supabase)")
        except Exception as e:
            logger.warning(f"[Database] save_pool_usage({pool_name}): Supabase error, falling back to JSON: {type(e).__name__}: {e}")
            try:
                with open(json_file, 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"[Database] save_pool_usage({pool_name}): JSON fallback successful ({len(data)} items)")
            except Exception as json_e:
                logger.error(f"[Database] save_pool_usage({pool_name}): JSON fallback failed: {type(json_e).__name__}: {json_e}")

    def increment_pool_usage(self, pool_name, response_id, response_text):
        """
        Generic usage increment for any response pool.

        Args:
            pool_name (str): Pool identifier
            response_id (str): Response ID
            response_text (str): Response text (updates if changed)

        Returns:
            int: New usage count
        """
        from datetime import datetime, timezone

        try:
            usage_data = self.load_pool_usage(pool_name)

            if response_id not in usage_data:
                usage_data[response_id] = {'text': response_text, 'usage_count': 0, 'last_used': None}
                logger.debug(f"[Database] increment_pool_usage({pool_name}): New response '{response_id}'")

            # Update both usage AND text (in case text was edited)
            usage_data[response_id]['text'] = response_text
            usage_data[response_id]['usage_count'] += 1
            usage_data[response_id]['last_used'] = datetime.now(timezone.utc).isoformat()
            new_count = usage_data[response_id]['usage_count']

            self.save_pool_usage(pool_name, usage_data)
            logger.debug(f"[Database] increment_pool_usage({pool_name}): '{response_id}' now at {new_count} uses")
            return new_count
        except Exception as e:
            logger.error(f"[Database] increment_pool_usage({pool_name}): Failed for '{response_id}': {type(e).__name__}: {e}")
            return 1

    def load_prebans(self):
        """Load prebanned user IDs from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('prebans.json', 'r') as f:
                    data = json.load(f)
                    # Count total prebans across all guilds
                    count = sum(len(users) for users in data.values())
                    logger.info(f"[Database] load_prebans: Success ({count} users from JSON)")
                    return data
            except FileNotFoundError:
                logger.info("[Database] load_prebans: No JSON file found, returning empty dict")
                return {}
            except Exception as e:
                logger.error(f"[Database] load_prebans: JSON read failed: {type(e).__name__}: {e}")
                return {}

        try:
            response = self.supabase.table('prebans').select("*").execute()
            prebans_dict = {}
            for item in response.data:
                guild_id = item['guild_id']
                user_id = item['user_id']
                if guild_id not in prebans_dict:
                    prebans_dict[guild_id] = {}
                prebans_dict[guild_id][user_id] = item['data']
            count = sum(len(users) for users in prebans_dict.values())
            logger.info(f"[Database] load_prebans: Success ({count} users from Supabase)")
            return prebans_dict
        except Exception as e:
            logger.error(f"[Database] load_prebans: Supabase query failed: {type(e).__name__}: {e}")
            return {}

    def save_prebans(self, data):
        """Save prebanned user IDs to Supabase or JSON"""
        count = sum(len(users) for users in data.values())

        if not self.supabase:
            try:
                with open('prebans.json', 'w') as f:
                    json.dump(data, f)
                logger.info(f"[Database] save_prebans: Success ({count} users to JSON)")
            except Exception as e:
                logger.error(f"[Database] save_prebans: JSON write failed: {type(e).__name__}: {e}")
            return

        try:
            # Clear existing
            self.supabase.table('prebans').delete().neq('guild_id', '0').execute()

            # Insert new data
            for guild_id, guild_prebans in data.items():
                for user_id, preban_data in guild_prebans.items():
                    self.supabase.table('prebans').upsert({
                        'guild_id': guild_id,
                        'user_id': user_id,
                        'data': preban_data
                    }).execute()
            logger.info(f"[Database] save_prebans: Success ({count} users to Supabase)")
        except Exception as e:
            logger.warning(f"[Database] save_prebans: Supabase error, falling back to JSON: {type(e).__name__}: {e}")
            try:
                with open('prebans.json', 'w') as f:
                    json.dump(data, f)
                logger.info(f"[Database] save_prebans: JSON fallback successful ({count} users)")
            except Exception as json_e:
                logger.error(f"[Database] save_prebans: JSON fallback failed: {type(json_e).__name__}: {json_e}")

# Create global instance
db = BotDatabase()

# Export functions
def load_reaction_roles():
    return db.load_reaction_roles()

def save_reaction_roles(data):
    db.save_reaction_roles(data)

def load_warnings():
    return db.load_warnings()

def save_warnings(data):
    db.save_warnings(data)

def load_suggestions():
    return db.load_suggestions()

def save_suggestions(data):
    db.save_suggestions(data)

def load_whisper_usage():
    return db.load_whisper_usage()

def save_whisper_usage(data):
    db.save_whisper_usage(data)

def increment_whisper_usage(whisper_id, whisper_text):
    return db.increment_whisper_usage(whisper_id, whisper_text)

def load_8ball_usage():
    return db.load_8ball_usage()

def save_8ball_usage(data):
    db.save_8ball_usage(data)

def increment_8ball_usage(response_id, response_text):
    return db.increment_8ball_usage(response_id, response_text)

def load_vague_usage():
    return db.load_vague_usage()

def save_vague_usage(data):
    db.save_vague_usage(data)

def increment_vague_usage(statement_id, statement_text):
    return db.increment_vague_usage(statement_id, statement_text)

def load_prebans():
    return db.load_prebans()

def save_prebans(data):
    db.save_prebans(data)

# Generic pool functions for intent-based response pools
def load_pool_usage(pool_name):
    return db.load_pool_usage(pool_name)

def save_pool_usage(pool_name, data):
    db.save_pool_usage(pool_name, data)

def increment_pool_usage(pool_name, response_id, response_text):
    return db.increment_pool_usage(pool_name, response_id, response_text)