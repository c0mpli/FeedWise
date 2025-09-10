import asyncio
import os
import sys
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv()

from browser_use import Agent, Browser, ChatOpenAI

TWITTER_USERNAME = os.getenv("TWITTER_USERNAME", "")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD", "")
POSTS_TO_OPTIMIZE = int(os.getenv("POSTS_TO_OPTIMIZE", "50"))
INTERESTS = os.getenv("INTERESTS", "development").split(",")

class InterestAction(BaseModel):
    topic: str
    action_taken: str
    posts_affected: int

class FeedOptimizationResult(BaseModel):
    interests_processed: List[str]
    actions_taken: List[InterestAction]
    feed_relevance_score: int
    recommendations_for_future: List[str]

# browser = Browser(
#     executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
#     user_data_dir='~/Library/Application Support/Google/Chrome',
#     profile_directory='Default',
# )

async def login_to_twitter():
    """Login to Twitter using credentials"""
    
    login_task = f"""
    Navigate to twitter.com and log in with the following credentials:
    Username/Email: {TWITTER_USERNAME}
    Password: {TWITTER_PASSWORD}
    
    Steps:
    1. Go to https://x.com/i/flow/login?lang=en
    2. Login with the username and password provided
    3. Handle any additional verification steps if they appear
    4. Wait until successfully logged in and on the main Twitter feed
    
    If you encounter 2FA or additional verification, wait for manual intervention.
    """
    
    agent = Agent(
        llm=ChatOpenAI(model='gpt-4o-mini'),
        task=login_task,
        # browser=browser,
        use_vision=True,

    )
    
    print("Logging into Twitter...")
    await agent.run()
    print("Login completed!")

async def cleanup_explore_feed():
    """Clean up Twitter explore feed based on interests"""
    
    interests_str = ", ".join(INTERESTS)
    
    cleanup_task = f"""
    Clean up the Twitter Explore feed to match these interests: {interests_str}
    Optimize exactly {POSTS_TO_OPTIMIZE} posts.
    
    Tasks to perform:
    1. Navigate to the Explore tab on Twitter
    2. Look through the trending topics and recommended content
    3. For each piece of content you see (up to {POSTS_TO_OPTIMIZE} posts total):
       - If it matches our interests ({interests_str}), engage with it by liking or retweeting
       - If it doesn't match our interests, use "Not interested" or "Show fewer tweets like this"
       - Click on relevant hashtags and topics to train the algorithm
    4. Search for each of our interest topics individually:
       - Search for "{INTERESTS[0]}"
       - Like and engage with high-quality tweets
       - Follow 2-3 relevant accounts posting about this topic
       - Repeat for other interests: {", ".join(INTERESTS[1:])}
    5. Go to Twitter Settings > Your account > Account information > Interests
       - Add/select topics that match our interests: {interests_str}
       - Remove unrelated interests
    6. Visit the "Topics" section and follow topics related to our interests
    
    IMPORTANT: Process exactly {POSTS_TO_OPTIMIZE} posts total across all activities.
    Return structured data about what actions were taken.
    """
    
    agent = Agent(
        llm=ChatOpenAI(model='gpt-4o-mini'),
        task=cleanup_task,
        # browser=browser,
        output_model_schema=FeedOptimizationResult,
        use_vision=True,
    )
    
    print("Cleaning up explore feed based on interests...")
    history = await agent.run()
    result = history.final_result()
    
    if result:
        parsed = FeedOptimizationResult.model_validate_json(result)
        print(f"\nFeed optimization completed!")
        print(f"Interests processed: {parsed.interests_processed}")
        print(f"Actions taken: {len(parsed.actions_taken)}")
        print(f"Feed relevance score: {parsed.feed_relevance_score}/100")
        
        print("\nDetailed actions:")
        for action in parsed.actions_taken:
            print(f"  - {action.topic}: {action.action_taken} ({action.posts_affected} posts)")
        
        print(f"\nRecommendations for future: {parsed.recommendations_for_future}")
        
        return parsed
    
    return None

async def main():
    """Main Twitter automation function"""
    try:
        print("=== Twitter Feed Automation ===")
        print(f"Target interests: {', '.join(INTERESTS)}")
        print()
        
        # Step 1: Login to Twitter
        await login_to_twitter()
        
        # Step 2: Clean up explore feed based on interests
        result = await cleanup_explore_feed()
        
        if result:
            print("\n=== Automation Complete ===")
            print("Your Twitter explore feed has been optimized!")
        else:
            print("\n=== Automation Failed ===")
            print("Could not complete feed optimization")
            
    except Exception as e:
        print(f"Error during automation: {e}")
    
    finally:
        print("\nClosing browser...")

if __name__ == '__main__':
    print("Starting Twitter automation...")
    print()
    asyncio.run(main())