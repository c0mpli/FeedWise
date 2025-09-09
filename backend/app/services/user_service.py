import os
import asyncio
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatOpenAI

# Load environment variables
load_dotenv()

# Disable telemetry
os.environ['ANONYMIZED_TELEMETRY'] = "false"


class TwitterLoginService:
    def __init__(self):
        # Load credentials from environment variables for security
        self.credentials = {
            'x_user': os.getenv('TWITTER_USERNAME'),  # or X_USERNAME
            'x_pass': os.getenv('TWITTER_PASSWORD')   # or X_PASSWORD
        }
        
        # Validate credentials are loaded
        if not self.credentials['x_user'] or not self.credentials['x_pass']:
            raise ValueError(
                "Twitter credentials not found. Please set TWITTER_USERNAME and TWITTER_PASSWORD in your .env file"
            )
        
        # Initialize LLM
        self.llm = ChatOpenAI(model='gpt-4o-mini')  # Fixed model name
    
    async def login_to_twitter(self):
        """Login to Twitter/X using browser automation"""
        
        # Option 1: Make credentials available for all websites
        sensitive_data = self.credentials
        
        # Option 2: Domain-specific credentials (more secure)
        # sensitive_data = {
        #     'https://*.twitter.com': self.credentials,
        #     'https://*.x.com': self.credentials,
        #     'https://twitter.com': self.credentials,
        #     'https://x.com': self.credentials,
        # }
        
        agent = Agent(
            task='Go to twitter.com (or x.com) and log in with username x_user and password x_pass',
            sensitive_data=sensitive_data,
            use_vision=False,  # Disable vision to prevent LLM seeing sensitive data in screenshots
            llm=self.llm,
        )
        
        try:
            result = await agent.run()
            print("✅ Successfully logged into Twitter!")
            return result
        except Exception as e:
            print(f"❌ Failed to login to Twitter: {str(e)}")
            raise
    
    async def login_and_perform_task(self, task_after_login):
        """Login to Twitter and then perform additional tasks using Chrome"""
        
        # Configure browser to use Chrome
        browser = Browser(
            browser_type="chromium",
            headless=False,
        )
        
        sensitive_data = self.credentials
        
        full_task = f"""
        Step 1: Login Process
        - Navigate to https://x.com/
        - Click on "Sign in" button
        - Enter username (x_user) and click "Next"
        - Enter password (x_pass) and click "Log in"
        
        Step 2: After successful login
        {task_after_login}
        """
        
        agent = Agent(
            task=full_task,
            sensitive_data=sensitive_data,
            browser=browser,  # Use Chrome browser
            use_vision=False,
            llm=self.llm,
        )
        
        try:
            result = await agent.run()
            print("✅ Successfully completed Twitter login and task!")
            return result
        except Exception as e:
            print(f"❌ Failed to complete Twitter task: {str(e)}")
            raise


async def main():
    """Example usage of the Twitter login service"""
    
    service = TwitterLoginService()
    
    try:
        # Option 1: Just login
        print("🔐 Logging into Twitter...")
        await service.login_to_twitter()
        
        # Option 2: Login and perform additional task
        # print("🔐 Logging into Twitter and posting a tweet...")
        # await service.login_and_perform_task("compose and post a tweet saying 'Hello from browser-use!'")
        
        # Option 3: Login and check notifications
        # print("🔐 Logging into Twitter and checking notifications...")
        # await service.login_and_perform_task("check my notifications and tell me how many unread notifications I have")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Make sure to add these to your .env file:")
        print("TWITTER_USERNAME=your-username@email.com")
        print("TWITTER_PASSWORD=your-password")
        print("OPENAI_API_KEY=your-openai-api-key")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
