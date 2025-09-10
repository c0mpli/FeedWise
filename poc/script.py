import asyncio
import os
import sys
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv()

from browser_use import Agent, Browser, ChatOpenAI

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
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

browser = Browser(highlight_elements=True)

async def login_and_optimize_instagram():
    """Login to Instagram and optimize the explore feed in one seamless flow"""
    
    interests_str = ", ".join(INTERESTS)
    
    complete_task = f"""
    Complete Instagram login and feed optimization task with these credentials and interests:
    Username: {INSTAGRAM_USERNAME}
    Password: {INSTAGRAM_PASSWORD}
    Target interests: {interests_str}
    Posts to optimize: {POSTS_TO_OPTIMIZE}
    
    PHASE 1: LOGIN
    1. Go to https://www.instagram.com/accounts/login/
    2. Enter the username: {INSTAGRAM_USERNAME}
    3. Enter the password: {INSTAGRAM_PASSWORD}
    4. Click the "Log In" button
    5. Handle any additional verification steps if they appear (dismiss "Save Info" prompts)
    6. Wait until successfully logged in and on the main Instagram feed
    
    PHASE 2: GET TOP USERS (research phase)
    1. Open a new tab and search for top Instagram users in each interest area:
       - Go to Google or any search engine in the new tab
       - Search for "top 10 Instagram users for {INTERESTS[0] if INTERESTS else 'development'}"
       - Find and collect the top 10 usernames for this interest
       - Repeat for each interest: {", ".join(INTERESTS[1:]) if len(INTERESTS) > 1 else 'No additional interests'}
       - Store all collected usernames (total of 10 usernames per interest)
    2. Close the research tab and return to the Instagram tab
    3. Follow the collected top users:
       - Use Instagram's search bar to find each collected username
       - Follow each of these top users
       - Like 2-3 of their recent posts to signal interest
    
    PHASE 3: FEED OPTIMIZATION
    1. Navigate to the Reels page on Instagram (click the reels/video icon at /reels)
    2. Optimize the Reels feed by looking through the reels and recommended content
    3. For each reel you see (up to {POSTS_TO_OPTIMIZE} reels total):
       - If it matches our interests ({interests_str}), engage with it by liking, saving, or sharing
       - If it doesn't match our interests, click the "Not Interested" option (three dots menu)
       - Click on relevant hashtags and topics in the reel descriptions to train the algorithm
       - IMPORTANT: After every 5 reel interactions, refresh the page to get fresh content
    4. Search for each of our interest topics individually in Reels:
       - Use the search bar to search for "{INTERESTS[0] if INTERESTS else 'development'}" and filter by Reels
       - Like and engage with high-quality reels about this topic
       - Follow 2-3 more relevant accounts creating reels about this topic
       - Refresh the page after every 5 interactions here as well
       - Repeat for other interests: {", ".join(INTERESTS[1:]) if len(INTERESTS) > 1 else 'No additional interests'}
    5. Go to your Profile > Settings > Account > Interests (if available)
       - Add topics that match our interests: {interests_str}
       - Remove unrelated interests if possible
    6. Follow relevant hashtags related to our interests
    
    IMPORTANT NOTES:
    - Follow the exact login sequence: username → next → password → login
    - If you encounter 2FA or additional verification, wait for manual intervention
    - Process exactly {POSTS_TO_OPTIMIZE} posts total across all feed optimization activities
    - Complete both phases in one continuous session
    - Return structured data about what actions were taken during optimization
    """
    
    agent = Agent(
        llm=ChatOpenAI(model='gpt-4o-mini'),
        task=complete_task,
        browser=browser,
        output_model_schema=FeedOptimizationResult,
        use_vision=True,
    )
    
    print("Starting Instagram login and feed optimization...")
    history = await agent.run()
    result = history.final_result()
    
    if result:
        parsed = FeedOptimizationResult.model_validate_json(result)
        print(f"\nInstagram optimization completed!")
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
    """Main Instagram automation function"""
    try:
        print("=== Instagram Feed Automation ===")
        print(f"Target interests: {', '.join(INTERESTS)}")
        print()
        
        # Complete login and feed optimization in one flow
        result = await login_and_optimize_instagram()
        
        if result:
            print("\n=== Automation Complete ===")
            print("Your Instagram explore feed has been optimized!")
        else:
            print("\n=== Automation Failed ===")
            print("Could not complete feed optimization")
            
    except Exception as e:
        print(f"Error during automation: {e}")
    
    finally:
        print("\nClosing browser...")

if __name__ == '__main__':
    print("Starting Instagram automation...")
    print()
    asyncio.run(main())