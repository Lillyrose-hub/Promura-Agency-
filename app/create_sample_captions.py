#!/usr/bin/env python3
"""
Create a sample Excel file with captions for testing the Caption Library
"""

import pandas as pd
from pathlib import Path

def create_sample_captions():
    """Create a sample Excel file with various caption categories"""

    # Sample data with categories and messages
    data = {
        'Category': [
            # Tip Prompts
            'Tip Prompt', 'Tip Prompt', 'Tip Prompt', 'Tip Prompt', 'Tip Prompt',

            # Mass Messages
            'Mass Message', 'Mass Message', 'Mass Message', 'Mass Message',

            # LIVE BOOST
            'LIVE BOOST', 'LIVE BOOST', 'LIVE BOOST',

            # Unlock Prompts
            'Unlock Prompt', 'Unlock Prompt', 'Unlock Prompt',

            # Bundle Prompts
            'Bundle Prompt', 'Bundle Prompt', 'Bundle Prompt',

            # PPV Captions
            'PPV Captions', 'PPV Captions', 'PPV Captions', 'PPV Captions',

            # Campaign Ideas
            'Campaign Ideas', 'Campaign Ideas', 'Campaign Ideas',

            # General
            'General', 'General', 'General', 'General'
        ],
        'Message': [
            # Tip Prompts
            "Hey babe! 💕 Your support means the world to me! Any tips are appreciated and keep me motivated to create more content for you 😘",
            "Feeling generous today? 💋 Every tip gets you closer to exclusive content!",
            "Want to make my day? 🥰 Show some love with a tip and I'll show you something special!",
            "Tips fuel my creativity! ⚡ Help me reach my goal today?",
            "Your tips = More content! 🔥 Let's make magic happen together!",

            # Mass Messages
            "Good morning beautiful! ☀️ Starting the day with some exclusive content just for my favorites! Check your DMs 💋",
            "FLASH SALE! 🎯 Next 24 hours only - 30% off all my premium content! Don't miss out!",
            "Missing you! 💔 Haven't heard from you in a while... everything okay?",
            "New content alert! 🚨 Just uploaded something VERY special to my vault!",

            # LIVE BOOST
            "🔴 GOING LIVE NOW! Join me for an intimate session! Limited spots available!",
            "LIVE in 30 minutes! 🎥 Who's ready for some fun? Interactive show starting soon!",
            "Last chance to join my LIVE! 🔥 Special surprises for everyone watching!",

            # Unlock Prompts
            "Want to see what's behind the blur? 😈 Unlock for a surprise!",
            "This one's too hot for the timeline! 🔥 Unlock to see the full version!",
            "Exclusive content inside! 💎 Only for my VIPs who unlock!",

            # Bundle Prompts
            "BUNDLE DEAL! 📦 Get 5 videos for the price of 3! Limited time offer!",
            "Special package just for you! 🎁 All my best content in one bundle!",
            "Weekend special! 💕 Unlock my premium bundle and save 40%!",

            # PPV Captions
            "NEW PPV! 🔥 10 minutes of pure pleasure! You don't want to miss this one!",
            "Exclusive video just for you! 💋 15 minutes of content you've been asking for!",
            "Special PPV drop! 😈 My hottest content yet - are you ready?",
            "Custom content available! 💕 Let me know what you want to see!",

            # Campaign Ideas
            "Tip Tuesday! Every tip today gets a special surprise in DMs! 💝",
            "Follower milestone celebration! 🎉 50% off everything this weekend!",
            "Birthday month special! 🎂 Join my VIP list for exclusive perks!",

            # General
            "Hey love! How's your day going? 💕",
            "Thanks for all your support! You make this journey amazing! 🥰",
            "What kind of content would you like to see more of? Let me know! 💭",
            "Feeling grateful for all my amazing supporters! You're the best! ⭐"
        ]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Create exports directory if it doesn't exist
    export_dir = Path("/root/onlysnarf-dashboard/app/exports")
    export_dir.mkdir(exist_ok=True)

    # Save to Excel file
    excel_file = export_dir / "sample_captions.xlsx"
    df.to_excel(excel_file, index=False, sheet_name="Captions")

    print(f"✅ Sample Excel file created: {excel_file}")
    print(f"📊 Total captions: {len(df)}")
    print(f"📁 Categories: {df['Category'].nunique()} unique categories")

    # Also create a simpler test file
    simple_data = {
        'Category': ['Tips', 'Mass', 'Live', 'General'],
        'Message': [
            'Thank you for your support! 💕',
            'New content available now!',
            'Going live in 10 minutes!',
            'How are you today?'
        ]
    }

    simple_df = pd.DataFrame(simple_data)
    simple_file = export_dir / "test_captions.xlsx"
    simple_df.to_excel(simple_file, index=False, sheet_name="Test")
    print(f"✅ Test file created: {simple_file}")

    return excel_file, simple_file

if __name__ == "__main__":
    create_sample_captions()