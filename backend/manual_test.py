#!/usr/bin/env python3
"""
Manual test script for OpenAI integration and opportunity detection.
Tests the AI service with sample communications and displays results.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ai_service import OpportunityDetector, AIServiceError
from app.services.opportunity_service import OpportunityService
from app.models.communication import CommunicationType
from app.utils.database import async_session_maker
from sqlalchemy import text


# Sample communications for testing
SAMPLE_COMMUNICATIONS = [
    {
        "client_name": "Acme Corp",
        "content": """Hi there,

We're opening a new Chicago office next month and need help with the commercial lease.
The space is about 5,000 square feet in the Loop. Also, we're planning to hire 20 new
employees for this location and need to review our employment contracts.

Looking forward to your help!

Best,
John Smith
CEO, Acme Corp""",
        "source_type": CommunicationType.EMAIL
    },
    {
        "client_name": "TechStart Inc",
        "content": """We're in discussions to acquire a smaller competitor, DataFlow Systems.
The deal is valued at approximately $2.5M. We need assistance with due diligence,
contract review, and ensuring all IP transfers properly. The target company has
15 employees that will be retained. Timeline is tight - we're hoping to close in 6 weeks.

Also need trademark registration for our new product line launching Q3.""",
        "source_type": CommunicationType.MEETING
    },
    {
        "client_name": "Global Manufacturing Ltd",
        "content": """Urgent: We've been served with a lawsuit from a former employee claiming
wrongful termination and discrimination. The complaint was filed yesterday in federal court.
We need litigation counsel immediately. The plaintiff is seeking $500K in damages.

Additionally, we're dealing with a patent infringement claim from a competitor regarding
our manufacturing process. Need IP litigation support as well.""",
        "source_type": CommunicationType.EMAIL
    }
]


async def test_ai_service():
    """Test AI service with sample communications"""
    print("=" * 80)
    print("MANUAL TEST: OpenAI Integration & Opportunity Detection")
    print("=" * 80)
    print()

    try:
        # Initialize AI detector
        print("Initializing AI Detector...")
        detector = OpportunityDetector()
        print("✓ AI Detector initialized successfully")
        print()

    except AIServiceError as e:
        print(f"✗ Failed to initialize AI Detector: {e}")
        print()
        print("Please ensure OPENAI_API_KEY is set in backend/.env file")
        return False

    # Test each sample communication
    for i, sample in enumerate(SAMPLE_COMMUNICATIONS, 1):
        print(f"Test Case {i}: {sample['client_name']}")
        print("-" * 80)
        print(f"Source: {sample['source_type'].value}")
        print(f"Content Preview: {sample['content'][:100]}...")
        print()

        try:
            # Analyze communication
            print("Analyzing communication with OpenAI...")
            opportunities = await detector.analyze_communication(
                content=sample['content'],
                client_name=sample['client_name']
            )

            print(f"✓ Analysis complete: Found {len(opportunities)} opportunities")
            print()

            # Display opportunities
            if opportunities:
                for j, opp in enumerate(opportunities, 1):
                    print(f"  Opportunity {j}:")
                    print(f"    Title:       {opp['title']}")
                    print(f"    Type:        {opp['type']}")
                    print(f"    Confidence:  {opp['confidence']}%")
                    print(f"    Description: {opp['description'][:100]}...")
                    if opp.get('estimated_value'):
                        print(f"    Est. Value:  {opp['estimated_value']}")
                    print(f"    Extracted:   {opp['extracted_text'][:80]}...")
                    print()
            else:
                print("  No opportunities detected (confidence threshold not met)")
                print()

        except Exception as e:
            print(f"✗ Error analyzing communication: {e}")
            print()
            return False

        print()

    return True


async def test_database_integration():
    """Test opportunity service with database"""
    print("=" * 80)
    print("DATABASE INTEGRATION TEST")
    print("=" * 80)
    print()

    try:
        # Get database session
        async with async_session_maker() as db:
            # Test database connection
            print("Testing database connection...")
            result = await db.execute(text("SELECT 1"))
            print("✓ Database connection successful")
            print()

            # Initialize services
            detector = OpportunityDetector()
            service = OpportunityService(db=db, ai_detector=detector)

            # Create communication with opportunities
            sample = SAMPLE_COMMUNICATIONS[0]
            print(f"Creating communication for {sample['client_name']}...")

            communication, opportunities = await service.create_communication_with_opportunities(
                content=sample['content'],
                client_name=sample['client_name'],
                source_type=sample['source_type']
            )

            print(f"✓ Communication created: ID={communication.id}")
            print(f"✓ {len(opportunities)} opportunities saved to database")
            print()

            # Display saved opportunities
            print("Saved Opportunities:")
            for i, opp in enumerate(opportunities, 1):
                print(f"  {i}. [{opp.opportunity_type.value}] {opp.title}")
                print(f"     Confidence: {float(opp.confidence)}%")
                print(f"     Notify: {'Yes' if service.should_notify(opp) else 'No'} (threshold: 70%)")
                print()

            # Verify count in database
            result = await db.execute(text("SELECT COUNT(*) FROM opportunities"))
            count = result.scalar()
            print(f"✓ Total opportunities in database: {count}")
            print()

    except Exception as e:
        print(f"✗ Database integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


async def main():
    """Run all tests"""
    print()
    print("Starting Manual Tests...")
    print()

    # Test AI service
    ai_success = await test_ai_service()

    if not ai_success:
        print("AI service tests failed. Skipping database tests.")
        sys.exit(1)

    # Test database integration
    db_success = await test_database_integration()

    print()
    print("=" * 80)
    if ai_success and db_success:
        print("✓ ALL TESTS PASSED")
        print()
        print("Next steps:")
        print("1. Start the server: uvicorn app.main:app --reload")
        print("2. Test GraphQL mutation at http://localhost:8000/graphql")
        print("3. Check database: docker-compose exec db psql -U nexl -d nexl_opportunities")
    else:
        print("✗ SOME TESTS FAILED")
        sys.exit(1)
    print("=" * 80)
    print()


if __name__ == "__main__":
    asyncio.run(main())
