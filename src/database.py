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