# test_pipeline.py
"""
Simple pipeline verification script to test:
1. Database initialization and operations
2. Prompt compilation logic
3. Offline model generation
"""

import sys
import os

# Ensure the current directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')


from prompt_template import compile_prompt, get_versions
from model import generate_copy
from database import init_db, save_history, get_history, update_quality_score, DB_NAME

def run_tests():
    print("🚀 Starting Automated Copywriting & Tone Transformer verification tests...")
    
    # Use a temporary database for testing
    test_db = "test_copywriting_history.db"
    if os.path.exists(test_db):
        os.remove(test_db)
        
    try:
        # Test 1: Database Initialization
        print("\n--- Test 1: Initializing Database ---")
        init_db(db_path=test_db)
        print("✅ Database initialized successfully.")
        
        # Test 2: Prompt Compilation
        print("\n--- Test 2: Compiling Prompts ---")
        product = "SolarBackpack"
        desc = "A backpack with built-in solar panels to charge devices on the go."
        platform = "Instagram"
        tone = "Creative"
        version = "v2.0 (Conversion Focused)"
        
        prompt = compile_prompt(product, desc, platform, tone, version)
        assert product in prompt, "Product name should be in the compiled prompt."
        assert tone in prompt, "Tone should be in the compiled prompt."
        assert "Instagram" in prompt, "Platform should be in the compiled prompt."
        print("✅ Prompt compiled successfully:")
        print(f"   [Preview]: {prompt[:100]}...")
        
        # Test 3: Demo Model Generation
        print("\n--- Test 3: Model Generation (Demo Mode) ---")
        generated = generate_copy(prompt, 0.7, 0.9, provider="Demo (Offline)")
        assert len(generated) > 50, "Generated text should be non-empty."
        assert "DEMO OFFLINE" in generated, "Should use demo mode."
        print("✅ Generated copy successfully:")
        print(f"   [Preview]: {generated[:150]}...")
        
        # Test 4: Saving to Database
        print("\n--- Test 4: Database Insertions ---")
        inserted_id = save_history(
            product_name=product,
            description=desc,
            platform=platform,
            tone=tone,
            prompt_version=version,
            prompt_compiled=prompt,
            generated_copy=generated,
            temperature=0.7,
            top_p=0.9,
            quality_score=0.0,
            db_path=test_db
        )
        print(f"✅ Record saved. Inserted ID: {inserted_id}")
        
        # Test 5: Fetching History
        print("\n--- Test 5: Querying Database ---")
        history = get_history(limit=5, db_path=test_db)
        assert len(history) == 1, "Should have 1 record in history."
        assert history[0]["product_name"] == product, "Data should match."
        print("✅ History queried successfully.")
        
        # Test 6: Updating Quality Score
        print("\n--- Test 6: Updating Quality Rating ---")
        update_quality_score(inserted_id, 8.5, db_path=test_db)
        history_updated = get_history(limit=5, db_path=test_db)
        assert history_updated[0]["quality_score"] == 8.5, "Quality score should be updated to 8.5."
        print("✅ Quality score updated successfully.")
        
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! The pipeline is fully functional.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        sys.exit(1)
        
    finally:
        # Clean up test database
        if os.path.exists(test_db):
            os.remove(test_db)
            print("\n🧹 Cleaned up temporary test database.")

if __name__ == "__main__":
    run_tests()
