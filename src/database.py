import os
import json
from supabase import create_client, Client

class BotDatabase:
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if url and key:
            self.supabase: Client = create_client(url, key)
            self.init_tables()
        else:
            print("WARNING: No Supabase credentials found, using JSON fallback")
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
                    return json.load(f)
            except:
                return {}
        
        try:
            response = self.supabase.table('reaction_roles').select("*").execute()
            return {item['message_id']: item['data'] for item in response.data}
        except:
            return {}
    
    def save_reaction_roles(self, data):
        """Save reaction roles to Supabase or JSON"""
        if not self.supabase:
            with open('reaction_roles.json', 'w') as f:
                json.dump(data, f)
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
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
            with open('reaction_roles.json', 'w') as f:
                json.dump(data, f)
    
    def load_warnings(self):
        """Load warnings from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('warnings.json', 'r') as f:
                    return json.load(f)
            except:
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
            return warnings_dict
        except:
            return {}
    
    def save_warnings(self, data):
        """Save warnings to Supabase or JSON"""
        if not self.supabase:
            with open('warnings.json', 'w') as f:
                json.dump(data, f)
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
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
            with open('warnings.json', 'w') as f:
                json.dump(data, f)

    def load_suggestions(self):
        """Load suggestions from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('suggestions.json', 'r') as f:
                    return json.load(f)
            except:
                return {}

        try:
            response = self.supabase.table('suggestions').select("*").execute()
            return {item['message_id']: item['data'] for item in response.data}
        except:
            return {}

    def save_suggestions(self, data):
        """Save suggestions to Supabase or JSON"""
        if not self.supabase:
            with open('suggestions.json', 'w') as f:
                json.dump(data, f)
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
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
            with open('suggestions.json', 'w') as f:
                json.dump(data, f)

    def load_whisper_usage(self):
        """Load whisper usage statistics from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('whisper_usage.json', 'r') as f:
                    return json.load(f)
            except:
                return {}

        try:
            response = self.supabase.table('whisper_usage').select("*").execute()
            # Return dict keyed by whisper_id
            return {item['whisper_id']: {
                'text': item['whisper_text'],
                'usage_count': item['usage_count'],
                'last_used': item['last_used']
            } for item in response.data}
        except:
            return {}

    def save_whisper_usage(self, data):
        """Save whisper usage statistics to Supabase or JSON"""
        if not self.supabase:
            with open('whisper_usage.json', 'w') as f:
                json.dump(data, f, indent=2)
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
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
            with open('whisper_usage.json', 'w') as f:
                json.dump(data, f, indent=2)

    def increment_whisper_usage(self, whisper_id, whisper_text):
        """Increment usage count for a whisper (ID-based)"""
        from datetime import datetime, timezone

        usage_data = self.load_whisper_usage()

        if whisper_id not in usage_data:
            usage_data[whisper_id] = {'text': whisper_text, 'usage_count': 0, 'last_used': None}

        # Update both usage AND text (in case text was edited in constants.py)
        usage_data[whisper_id]['text'] = whisper_text
        usage_data[whisper_id]['usage_count'] += 1
        usage_data[whisper_id]['last_used'] = datetime.now(timezone.utc).isoformat()

        self.save_whisper_usage(usage_data)
        return usage_data[whisper_id]['usage_count']

    def load_8ball_usage(self):
        """Load 8-ball response usage statistics from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('8ball_usage.json', 'r') as f:
                    return json.load(f)
            except:
                return {}

        try:
            response = self.supabase.table('response_8ball_usage').select("*").execute()
            # Return dict keyed by response_id
            return {item['response_id']: {
                'text': item['response_text'],
                'usage_count': item['usage_count'],
                'last_used': item['last_used']
            } for item in response.data}
        except:
            return {}

    def save_8ball_usage(self, data):
        """Save 8-ball response usage statistics to Supabase or JSON"""
        if not self.supabase:
            with open('8ball_usage.json', 'w') as f:
                json.dump(data, f, indent=2)
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
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
            with open('8ball_usage.json', 'w') as f:
                json.dump(data, f, indent=2)

    def increment_8ball_usage(self, response_id, response_text):
        """Increment usage count for an 8-ball response (ID-based)"""
        from datetime import datetime, timezone

        usage_data = self.load_8ball_usage()

        if response_id not in usage_data:
            usage_data[response_id] = {'text': response_text, 'usage_count': 0, 'last_used': None}

        # Update both usage AND text (in case text was edited in constants.py)
        usage_data[response_id]['text'] = response_text
        usage_data[response_id]['usage_count'] += 1
        usage_data[response_id]['last_used'] = datetime.now(timezone.utc).isoformat()

        self.save_8ball_usage(usage_data)
        return usage_data[response_id]['usage_count']

    def load_vague_usage(self):
        """Load vague statement usage statistics from Supabase or JSON"""
        if not self.supabase:
            try:
                with open('vague_usage.json', 'r') as f:
                    return json.load(f)
            except:
                return {}

        try:
            response = self.supabase.table('response_vague_usage').select("*").execute()
            # Return dict keyed by statement_id
            return {item['statement_id']: {
                'text': item['statement_text'],
                'usage_count': item['usage_count'],
                'last_used': item['last_used']
            } for item in response.data}
        except:
            return {}

    def save_vague_usage(self, data):
        """Save vague statement usage statistics to Supabase or JSON"""
        if not self.supabase:
            with open('vague_usage.json', 'w') as f:
                json.dump(data, f, indent=2)
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
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
            with open('vague_usage.json', 'w') as f:
                json.dump(data, f, indent=2)

    def increment_vague_usage(self, statement_id, statement_text):
        """Increment usage count for a vague statement (ID-based)"""
        from datetime import datetime, timezone

        usage_data = self.load_vague_usage()

        if statement_id not in usage_data:
            usage_data[statement_id] = {'text': statement_text, 'usage_count': 0, 'last_used': None}

        # Update both usage AND text (in case text was edited in constants.py)
        usage_data[statement_id]['text'] = statement_text
        usage_data[statement_id]['usage_count'] += 1
        usage_data[statement_id]['last_used'] = datetime.now(timezone.utc).isoformat()

        self.save_vague_usage(usage_data)
        return usage_data[statement_id]['usage_count']

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