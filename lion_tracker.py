"""
Lion Scout Advancement Tracker
A Streamlit application for tracking Lion Scout (Kindergarten) advancement progress.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

DATA_DIR = Path("tracker_data")
ROSTER_FILE = DATA_DIR / "Roster.csv"
REQUIREMENT_KEY_FILE = DATA_DIR / "Requirement_Key.csv"
MEETINGS_FILE = DATA_DIR / "Meetings.csv"
ATTENDANCE_FILE = DATA_DIR / "Meeting_Attendance.csv"

# Static data: Official BSA Lion Scout requirements
# Required Adventures (6 total - must complete all 6)
# Elective Adventures (14 total - must complete any 2)
LION_REQUIREMENTS = [
    # ========== REQUIRED ADVENTURES ==========

    # Bobcat (Required - 4 requirements)
    {"Req_ID": "Bobcat.1", "Adventure": "Bobcat", "Requirement_Description": "1. Get to know the members of your den", "Required": True},
    {"Req_ID": "Bobcat.2", "Adventure": "Bobcat", "Requirement_Description": "2. Have your Lion adult partner or den leader read the Scout Law to you. Demonstrate your understanding of being friendly", "Required": True},
    {"Req_ID": "Bobcat.3", "Adventure": "Bobcat", "Requirement_Description": "3. Share with your Lion adult partner, during a den meeting or at home, a time when you have demonstrated the Cub Scout motto 'Do Your Best'", "Required": True},
    {"Req_ID": "Bobcat.4", "Adventure": "Bobcat", "Requirement_Description": "4. At home, with your parent or legal guardian, do the activities in the booklet 'How to Protect Your Children from Child Abuse: A Parent's Guide'", "Required": True},

    # Fun on the Run (Required - 4 requirements)
    {"Req_ID": "FunOnTheRun.1", "Adventure": "Fun on the Run", "Requirement_Description": "1. Identify the five different food groups", "Required": True},
    {"Req_ID": "FunOnTheRun.2", "Adventure": "Fun on the Run", "Requirement_Description": "2. Practice hand washing. Point out when you should wash your hands", "Required": True},
    {"Req_ID": "FunOnTheRun.3", "Adventure": "Fun on the Run", "Requirement_Description": "3. Be active for 20 minutes", "Required": True},
    {"Req_ID": "FunOnTheRun.4", "Adventure": "Fun on the Run", "Requirement_Description": "4. Practice methods that help you rest", "Required": True},

    # Lion's Roar (Required - 4 requirements)
    {"Req_ID": "LionsRoar.1", "Adventure": "Lion's Roar", "Requirement_Description": "1. With permission from your parent or legal guardian watch the Protect Yourself Rules video for the Lion rank", "Required": True},
    {"Req_ID": "LionsRoar.2", "Adventure": "Lion's Roar", "Requirement_Description": "2. With your Lion adult partner, demonstrate Shout, Run, Tell as explained in the Protect Yourself Rules video", "Required": True},
    {"Req_ID": "LionsRoar.3", "Adventure": "Lion's Roar", "Requirement_Description": "3. With your Lion adult partner, demonstrate how to access emergency services", "Required": True},
    {"Req_ID": "LionsRoar.4", "Adventure": "Lion's Roar", "Requirement_Description": "4. With your Lion adult partner, demonstrate how to safely cross a street or walk in a parking lot", "Required": True},

    # Lion's Pride (Required - 3 requirements)
    {"Req_ID": "LionsPride.1", "Adventure": "Lion's Pride", "Requirement_Description": "1. With your parent or legal guardian talk about your family's faith traditions. Draw a picture of your favorite family's faith tradition holiday or celebration", "Required": True},
    {"Req_ID": "LionsPride.2", "Adventure": "Lion's Pride", "Requirement_Description": "2. With your family, attend a religious service OR other gathering that shows how your family expresses Family & Reverence", "Required": True},
    {"Req_ID": "LionsPride.3", "Adventure": "Lion's Pride", "Requirement_Description": "3. Make a cheerful card or a drawing for someone you love and give it to them", "Required": True},

    # King of the Jungle (Required - 4 requirements)
    {"Req_ID": "KingOfTheJungle.1", "Adventure": "King of the Jungle", "Requirement_Description": "1. Draw a picture or take a photo of the people you live with", "Required": True},
    {"Req_ID": "KingOfTheJungle.2", "Adventure": "King of the Jungle", "Requirement_Description": "2. With your Lion adult partner, choose a job that will help your family. Follow through by doing that job at least once", "Required": True},
    {"Req_ID": "KingOfTheJungle.3", "Adventure": "King of the Jungle", "Requirement_Description": "3. Talk with a grandparent or other older adult about what citizenship means to them", "Required": True},
    {"Req_ID": "KingOfTheJungle.4", "Adventure": "King of the Jungle", "Requirement_Description": "4. Participate in a service project", "Required": True},

    # Mountain Lion (Required - 4 requirements)
    {"Req_ID": "MountainLion.1", "Adventure": "Mountain Lion", "Requirement_Description": "1. Identify the Cub Scout Six Essentials. Show what you do with each item", "Required": True},
    {"Req_ID": "MountainLion.2", "Adventure": "Mountain Lion", "Requirement_Description": "2. With your den, pack, or family, take a walk outside spending for at least 20 minutes exploring the outdoors with your Cub Scout Six Essentials", "Required": True},
    {"Req_ID": "MountainLion.3", "Adventure": "Mountain Lion", "Requirement_Description": "3. Discover what S.A.W. means", "Required": True},
    {"Req_ID": "MountainLion.4", "Adventure": "Mountain Lion", "Requirement_Description": "4. Identify common animals that are found where you live. Separate those animals into domesticated and wild", "Required": True},

    # ========== ELECTIVE ADVENTURES ==========

    # Build It Up, Knock It Down (Elective - 3 requirements)
    {"Req_ID": "BuildItUp.1", "Adventure": "Build It Up, Knock It Down", "Requirement_Description": "1. With your Lion adult partner, build a structure", "Required": False},
    {"Req_ID": "BuildItUp.2", "Adventure": "Build It Up, Knock It Down", "Requirement_Description": "2. With your den or family, build a structure", "Required": False},
    {"Req_ID": "BuildItUp.3", "Adventure": "Build It Up, Knock It Down", "Requirement_Description": "3. Build something that is designed to be knocked down", "Required": False},

    # Champions for Nature (Elective - 4 requirements)
    {"Req_ID": "ChampionsNature.1", "Adventure": "Champions for Nature", "Requirement_Description": "1. Discover the difference between natural resources and man-made items", "Required": False},
    {"Req_ID": "ChampionsNature.2", "Adventure": "Champions for Nature", "Requirement_Description": "2. Discover the difference between organic, paper, plastic, metal and glass waste", "Required": False},
    {"Req_ID": "ChampionsNature.3", "Adventure": "Champions for Nature", "Requirement_Description": "3. Discover recycling", "Required": False},
    {"Req_ID": "ChampionsNature.4", "Adventure": "Champions for Nature", "Requirement_Description": "4. Participate in a conservation service project", "Required": False},

    # Count On Me (Elective - 3 requirements)
    {"Req_ID": "CountOnMe.1", "Adventure": "Count On Me", "Requirement_Description": "1. Make a Lion using only squares, triangles, and circles", "Required": False},
    {"Req_ID": "CountOnMe.2", "Adventure": "Count On Me", "Requirement_Description": "2. Play a game with your Lion adult partner or den that is based on counting or numbers", "Required": False},
    {"Req_ID": "CountOnMe.3", "Adventure": "Count On Me", "Requirement_Description": "3. Organize a group of items based on shape, then based on color, and one other category", "Required": False},

    # Everyday Tech (Elective - 3 requirements)
    {"Req_ID": "EverydayTech.1", "Adventure": "Everyday Tech", "Requirement_Description": "1. Discover the different types of technology you use everyday", "Required": False},
    {"Req_ID": "EverydayTech.2", "Adventure": "Everyday Tech", "Requirement_Description": "2. Learn about digital safety and how to protect yourself online", "Required": False},
    {"Req_ID": "EverydayTech.3", "Adventure": "Everyday Tech", "Requirement_Description": "3. Show how you can use technology safely", "Required": False},

    # Gizmos and Gadgets (Elective - 3 requirements)
    {"Req_ID": "GizmosGadgets.1", "Adventure": "Gizmos and Gadgets", "Requirement_Description": "1. Explore properties of motion", "Required": False},
    {"Req_ID": "GizmosGadgets.2", "Adventure": "Gizmos and Gadgets", "Requirement_Description": "2. Explore properties of force", "Required": False},
    {"Req_ID": "GizmosGadgets.3", "Adventure": "Gizmos and Gadgets", "Requirement_Description": "3. Use household materials to create a useful object", "Required": False},

    # Go Fish (Elective - 3 requirements)
    {"Req_ID": "GoFish.1", "Adventure": "Go Fish", "Requirement_Description": "1. Discover the different safety rules when you are near or in the water", "Required": False},
    {"Req_ID": "GoFish.2", "Adventure": "Go Fish", "Requirement_Description": "2. Draw a picture of a fish. Show your den at your den meeting", "Required": False},
    {"Req_ID": "GoFish.3", "Adventure": "Go Fish", "Requirement_Description": "3. Go on a fishing adventure and catch a fish. Or if you can't go fishing, discover different types of fish in your state", "Required": False},

    # I'll Do It Myself (Elective - 3 requirements)
    {"Req_ID": "IllDoItMyself.1", "Adventure": "I'll Do It Myself", "Requirement_Description": "1. Show you can do some things all by yourself. Create a Lion bag to hold items you can use to get ready in the morning", "Required": False},
    {"Req_ID": "IllDoItMyself.2", "Adventure": "I'll Do It Myself", "Requirement_Description": "2. Create your own personal care checklist that you can use every day", "Required": False},
    {"Req_ID": "IllDoItMyself.3", "Adventure": "I'll Do It Myself", "Requirement_Description": "3. Show how to tie your shoes", "Required": False},

    # Let's Camp Lion (Elective - 4 requirements)
    {"Req_ID": "LetsCampLion.1", "Adventure": "Let's Camp Lion", "Requirement_Description": "1. With your Lion adult partner, demonstrate the buddy system", "Required": False},
    {"Req_ID": "LetsCampLion.2", "Adventure": "Let's Camp Lion", "Requirement_Description": "2. Show what to do if the weather gets bad while you are camping", "Required": False},
    {"Req_ID": "LetsCampLion.3", "Adventure": "Let's Camp Lion", "Requirement_Description": "3. With the help of an adult, pack the things that will be needed for a campout", "Required": False},
    {"Req_ID": "LetsCampLion.4", "Adventure": "Let's Camp Lion", "Requirement_Description": "4. Go on a campout with your den or family", "Required": False},

    # On a Roll (Elective - 3 requirements)
    {"Req_ID": "OnARoll.1", "Adventure": "On a Roll", "Requirement_Description": "1. Identify safety equipment when riding a bicycle", "Required": False},
    {"Req_ID": "OnARoll.2", "Adventure": "On a Roll", "Requirement_Description": "2. Learn about the safety rules when riding a bicycle", "Required": False},
    {"Req_ID": "OnARoll.3", "Adventure": "On a Roll", "Requirement_Description": "3. Ride a bicycle or use roller skates, scooters, or skateboards safely while wearing safety equipment", "Required": False},

    # On Your Mark (Elective - 3 requirements)
    {"Req_ID": "OnYourMark.1", "Adventure": "On Your Mark", "Requirement_Description": "1. Play a game or do an activity with your den that requires teamwork", "Required": False},
    {"Req_ID": "OnYourMark.2", "Adventure": "On Your Mark", "Requirement_Description": "2. Do an obstacle course or a relay race with your den", "Required": False},
    {"Req_ID": "OnYourMark.3", "Adventure": "On Your Mark", "Requirement_Description": "3. Build and race a box derby car", "Required": False},

    # Pick My Path (Elective - 3 requirements)
    {"Req_ID": "PickMyPath.1", "Adventure": "Pick My Path", "Requirement_Description": "1. Explore the difference between choices and consequences", "Required": False},
    {"Req_ID": "PickMyPath.2", "Adventure": "Pick My Path", "Requirement_Description": "2. Practice doing a good turn daily", "Required": False},
    {"Req_ID": "PickMyPath.3", "Adventure": "Pick My Path", "Requirement_Description": "3. Play a game with your den about making good choices and understanding the rules", "Required": False},

    # Race Time Lion (Elective - 4 requirements)
    {"Req_ID": "RaceTimeLion.1", "Adventure": "Race Time Lion", "Requirement_Description": "1. Build a car or a boat with your den or with your Lion adult partner", "Required": False},
    {"Req_ID": "RaceTimeLion.2", "Adventure": "Race Time Lion", "Requirement_Description": "2. Learn the rules for your race", "Required": False},
    {"Req_ID": "RaceTimeLion.3", "Adventure": "Race Time Lion", "Requirement_Description": "3. Demonstrate good sportsmanship during your race", "Required": False},
    {"Req_ID": "RaceTimeLion.4", "Adventure": "Race Time Lion", "Requirement_Description": "4. Participate in a pack race", "Required": False},

    # Ready, Set, Grow (Elective - 3 requirements)
    {"Req_ID": "ReadySetGrow.1", "Adventure": "Ready, Set, Grow", "Requirement_Description": "1. Learn about the different sources of food such as plants, animals, or farms", "Required": False},
    {"Req_ID": "ReadySetGrow.2", "Adventure": "Ready, Set, Grow", "Requirement_Description": "2. Plant a garden in a pot or a patch. Explore the things that are needed to keep a plant alive and help it grow", "Required": False},
    {"Req_ID": "ReadySetGrow.3", "Adventure": "Ready, Set, Grow", "Requirement_Description": "3. Visit a farm, garden, orchard, ranch, or zoo. Share what you learned about plants or animals with your den or family", "Required": False},

    # Time to Swim (Elective - 5 requirements)
    {"Req_ID": "TimeToSwim.1", "Adventure": "Time to Swim", "Requirement_Description": "1. Discover the safety rules for swimming", "Required": False},
    {"Req_ID": "TimeToSwim.2", "Adventure": "Time to Swim", "Requirement_Description": "2. Show how you enter a pool safely", "Required": False},
    {"Req_ID": "TimeToSwim.3", "Adventure": "Time to Swim", "Requirement_Description": "3. Be active in the water for 20 minutes with your family or den", "Required": False},
    {"Req_ID": "TimeToSwim.4", "Adventure": "Time to Swim", "Requirement_Description": "4. Put your face under water and blow bubbles", "Required": False},
    {"Req_ID": "TimeToSwim.5", "Adventure": "Time to Swim", "Requirement_Description": "5. Show how you can exit a pool safely", "Required": False},
]

# Tiger Scout Requirements (1st Grade)
TIGER_REQUIREMENTS = [
    # Required Adventures (6 total)
    {"Req_ID": "Bobcat.1", "Adventure": "Bobcat", "Requirement_Description": "Complete Bobcat requirements", "Required": True},
    {"Req_ID": "TigerBites.1", "Adventure": "Tiger Bites", "Requirement_Description": "Complete Tiger Bites requirements (Personal Fitness)", "Required": True},
    {"Req_ID": "TigersRoar.1", "Adventure": "Tiger's Roar", "Requirement_Description": "Complete Tiger's Roar requirements (Personal Safety)", "Required": True},
    {"Req_ID": "TigerCircles.1", "Adventure": "Tiger Circles", "Requirement_Description": "Complete Tiger Circles requirements (Family & Reverence)", "Required": True},
    {"Req_ID": "TeamTiger.1", "Adventure": "Team Tiger", "Requirement_Description": "Complete Team Tiger requirements (Citizenship)", "Required": True},
    {"Req_ID": "TigersInTheWild.1", "Adventure": "Tigers in the Wild", "Requirement_Description": "Complete Tigers in the Wild requirements (Outdoors)", "Required": True},

    # Elective Adventures (Complete any 2)
    {"Req_ID": "ChampionsNatureTiger.1", "Adventure": "Champions for Nature Tiger", "Requirement_Description": "Complete Champions for Nature Tiger requirements", "Required": False},
    {"Req_ID": "CuriosityIntrigue.1", "Adventure": "Curiosity, Intrigue, and Magical Mysteries", "Requirement_Description": "Complete Curiosity, Intrigue, and Magical Mysteries requirements", "Required": False},
    {"Req_ID": "DesignedByTiger.1", "Adventure": "Designed by Tiger", "Requirement_Description": "Complete Designed by Tiger requirements", "Required": False},
    {"Req_ID": "FishOn.1", "Adventure": "Fish On", "Requirement_Description": "Complete Fish On requirements", "Required": False},
    {"Req_ID": "FloatsBoats.1", "Adventure": "Floats and Boats", "Requirement_Description": "Complete Floats and Boats requirements", "Required": False},
    {"Req_ID": "GoodKnights.1", "Adventure": "Good Knights", "Requirement_Description": "Complete Good Knights requirements", "Required": False},
    {"Req_ID": "LetsCampTiger.1", "Adventure": "Let's Camp Tiger", "Requirement_Description": "Complete Let's Camp Tiger requirements", "Required": False},
    {"Req_ID": "RaceTimeTiger.1", "Adventure": "Race Time Tiger", "Requirement_Description": "Complete Race Time Tiger requirements", "Required": False},
    {"Req_ID": "RollingTigers.1", "Adventure": "Rolling Tigers", "Requirement_Description": "Complete Rolling Tigers requirements", "Required": False},
    {"Req_ID": "SafeAndSmart.1", "Adventure": "Safe and Smart", "Requirement_Description": "Complete Safe and Smart requirements", "Required": False},
    {"Req_ID": "SkyIsTheLimit.1", "Adventure": "Sky is the Limit", "Requirement_Description": "Complete Sky is the Limit requirements", "Required": False},
    {"Req_ID": "StoriesInShapes.1", "Adventure": "Stories in Shapes", "Requirement_Description": "Complete Stories in Shapes requirements", "Required": False},
    {"Req_ID": "SummertimeFunTiger.1", "Adventure": "Summertime Fun Tiger", "Requirement_Description": "Complete Summertime Fun Tiger requirements", "Required": False},
    {"Req_ID": "TechAllAround.1", "Adventure": "Tech All Around", "Requirement_Description": "Complete Tech All Around requirements", "Required": False},
    {"Req_ID": "TigerTag.1", "Adventure": "Tiger Tag", "Requirement_Description": "Complete Tiger Tag requirements", "Required": False},
    {"Req_ID": "Tigeriffic.1", "Adventure": "Tiger-iffic!", "Requirement_Description": "Complete Tiger-iffic! requirements", "Required": False},
    {"Req_ID": "TigersInTheWater.1", "Adventure": "Tigers in the Water", "Requirement_Description": "Complete Tigers in the Water requirements", "Required": False},
]

# Wolf Scout Requirements (2nd Grade)
WOLF_REQUIREMENTS = [
    # Required Adventures (6 total)
    {"Req_ID": "Bobcat.1", "Adventure": "Bobcat", "Requirement_Description": "Complete Bobcat requirements", "Required": True},
    {"Req_ID": "RunningWithThePack.1", "Adventure": "Running With the Pack", "Requirement_Description": "Complete Running With the Pack requirements (Personal Fitness)", "Required": True},
    {"Req_ID": "SafetyInNumbers.1", "Adventure": "Safety in Numbers", "Requirement_Description": "Complete Safety in Numbers requirements (Personal Safety)", "Required": True},
    {"Req_ID": "Footsteps.1", "Adventure": "Footsteps", "Requirement_Description": "Complete Footsteps requirements (Family & Reverence)", "Required": True},
    {"Req_ID": "CouncilFire.1", "Adventure": "Council Fire", "Requirement_Description": "Complete Council Fire requirements (Citizenship)", "Required": True},
    {"Req_ID": "PawsOnThePath.1", "Adventure": "Paws on the Path", "Requirement_Description": "Complete Paws on the Path requirements (Outdoors)", "Required": True},

    # Elective Adventures (Complete any 2)
    {"Req_ID": "AWolfGoesFishing.1", "Adventure": "A Wolf Goes Fishing", "Requirement_Description": "Complete A Wolf Goes Fishing requirements", "Required": False},
    {"Req_ID": "AdventuresInCoins.1", "Adventure": "Adventures in Coins", "Requirement_Description": "Complete Adventures in Coins requirements", "Required": False},
    {"Req_ID": "AirOfTheWolf.1", "Adventure": "Air of the Wolf", "Requirement_Description": "Complete Air of the Wolf requirements", "Required": False},
    {"Req_ID": "ChampionsNatureWolf.1", "Adventure": "Champions for Nature Wolf", "Requirement_Description": "Complete Champions for Nature Wolf requirements", "Required": False},
    {"Req_ID": "CodeOfTheWolf.1", "Adventure": "Code of the Wolf", "Requirement_Description": "Complete Code of the Wolf requirements", "Required": False},
    {"Req_ID": "ComputingWolves.1", "Adventure": "Computing Wolves", "Requirement_Description": "Complete Computing Wolves requirements", "Required": False},
    {"Req_ID": "CubsWhoCare.1", "Adventure": "Cubs Who Care", "Requirement_Description": "Complete Cubs Who Care requirements", "Required": False},
    {"Req_ID": "DiggingInThePast.1", "Adventure": "Digging in the Past", "Requirement_Description": "Complete Digging in the Past requirements", "Required": False},
    {"Req_ID": "FindingYourWay.1", "Adventure": "Finding Your Way", "Requirement_Description": "Complete Finding Your Way requirements", "Required": False},
    {"Req_ID": "GermsAlive.1", "Adventure": "Germs Alive!", "Requirement_Description": "Complete Germs Alive! requirements", "Required": False},
    {"Req_ID": "LetsCampWolf.1", "Adventure": "Let's Camp Wolf", "Requirement_Description": "Complete Let's Camp Wolf requirements", "Required": False},
    {"Req_ID": "PawsForWater.1", "Adventure": "Paws for Water", "Requirement_Description": "Complete Paws for Water requirements", "Required": False},
    {"Req_ID": "PawsOfSkill.1", "Adventure": "Paws of Skill", "Requirement_Description": "Complete Paws of Skill requirements", "Required": False},
    {"Req_ID": "PedalWithThePack.1", "Adventure": "Pedal With the Pack", "Requirement_Description": "Complete Pedal With the Pack requirements", "Required": False},
    {"Req_ID": "RaceTimeWolf.1", "Adventure": "Race Time Wolf", "Requirement_Description": "Complete Race Time Wolf requirements", "Required": False},
    {"Req_ID": "SpiritOfTheWater.1", "Adventure": "Spirit of the Water", "Requirement_Description": "Complete Spirit of the Water requirements", "Required": False},
    {"Req_ID": "SummertimeFunWolf.1", "Adventure": "Summertime Fun Wolf", "Requirement_Description": "Complete Summertime Fun Wolf requirements", "Required": False},
]

# Bear Scout Requirements (3rd Grade)
BEAR_REQUIREMENTS = [
    # Required Adventures (6 total)
    {"Req_ID": "Bobcat.1", "Adventure": "Bobcat", "Requirement_Description": "Complete Bobcat requirements", "Required": True},
    {"Req_ID": "BearStrong.1", "Adventure": "Bear Strong", "Requirement_Description": "Complete Bear Strong requirements (Personal Fitness)", "Required": True},
    {"Req_ID": "StandingTall.1", "Adventure": "Standing Tall", "Requirement_Description": "Complete Standing Tall requirements (Personal Safety)", "Required": True},
    {"Req_ID": "Fellowship.1", "Adventure": "Fellowship", "Requirement_Description": "Complete Fellowship requirements (Family & Reverence)", "Required": True},
    {"Req_ID": "PawsForAction.1", "Adventure": "Paws for Action", "Requirement_Description": "Complete Paws for Action requirements (Citizenship)", "Required": True},
    {"Req_ID": "BearHabitat.1", "Adventure": "Bear Habitat", "Requirement_Description": "Complete Bear Habitat requirements (Outdoors)", "Required": True},

    # Elective Adventures (Complete any 2)
    {"Req_ID": "ABearGoesFishing.1", "Adventure": "A Bear Goes Fishing", "Requirement_Description": "Complete A Bear Goes Fishing requirements", "Required": False},
    {"Req_ID": "BalancingBears.1", "Adventure": "Balancing Bears", "Requirement_Description": "Complete Balancing Bears requirements", "Required": False},
    {"Req_ID": "BalooTheBuilder.1", "Adventure": "Baloo the Builder", "Requirement_Description": "Complete Baloo the Builder requirements", "Required": False},
    {"Req_ID": "BearsAfloat.1", "Adventure": "Bears Afloat", "Requirement_Description": "Complete Bears Afloat requirements", "Required": False},
    {"Req_ID": "BearsOnBikes.1", "Adventure": "Bears on Bikes", "Requirement_Description": "Complete Bears on Bikes requirements", "Required": False},
    {"Req_ID": "ChampionsNatureBear.1", "Adventure": "Champions for Nature Bear", "Requirement_Description": "Complete Champions for Nature Bear requirements", "Required": False},
    {"Req_ID": "ChefTech.1", "Adventure": "Chef Tech", "Requirement_Description": "Complete Chef Tech requirements", "Required": False},
    {"Req_ID": "CritterCare.1", "Adventure": "Critter Care", "Requirement_Description": "Complete Critter Care requirements", "Required": False},
    {"Req_ID": "Forensics.1", "Adventure": "Forensics", "Requirement_Description": "Complete Forensics requirements", "Required": False},
    {"Req_ID": "LetsCampBear.1", "Adventure": "Let's Camp Bear", "Requirement_Description": "Complete Let's Camp Bear requirements", "Required": False},
    {"Req_ID": "MarbleMadness.1", "Adventure": "Marble Madness", "Requirement_Description": "Complete Marble Madness requirements", "Required": False},
    {"Req_ID": "RaceTimeBear.1", "Adventure": "Race Time Bear", "Requirement_Description": "Complete Race Time Bear requirements", "Required": False},
    {"Req_ID": "RoaringLaughter.1", "Adventure": "Roaring Laughter", "Requirement_Description": "Complete Roaring Laughter requirements", "Required": False},
    {"Req_ID": "SalmonRun.1", "Adventure": "Salmon Run", "Requirement_Description": "Complete Salmon Run requirements", "Required": False},
    {"Req_ID": "SummertimeFunBear.1", "Adventure": "Summertime Fun Bear", "Requirement_Description": "Complete Summertime Fun Bear requirements", "Required": False},
    {"Req_ID": "SuperScience.1", "Adventure": "Super Science", "Requirement_Description": "Complete Super Science requirements", "Required": False},
    {"Req_ID": "Whittling.1", "Adventure": "Whittling", "Requirement_Description": "Complete Whittling requirements", "Required": False},
]

# Webelos Scout Requirements (4th Grade)
WEBELOS_REQUIREMENTS = [
    # Required Adventures (6 total)
    {"Req_ID": "Bobcat.1", "Adventure": "Bobcat", "Requirement_Description": "Complete Bobcat requirements", "Required": True},
    {"Req_ID": "StrongerFasterHigher.1", "Adventure": "Stronger, Faster, Higher", "Requirement_Description": "Complete Stronger, Faster, Higher requirements (Personal Fitness)", "Required": True},
    {"Req_ID": "MySafety.1", "Adventure": "My Safety", "Requirement_Description": "Complete My Safety requirements (Personal Safety)", "Required": True},
    {"Req_ID": "MyFamily.1", "Adventure": "My Family", "Requirement_Description": "Complete My Family requirements (Family & Reverence)", "Required": True},
    {"Req_ID": "MyCommunity.1", "Adventure": "My Community", "Requirement_Description": "Complete My Community requirements (Citizenship)", "Required": True},
    {"Req_ID": "WebelosWalkabout.1", "Adventure": "Webelos Walkabout", "Requirement_Description": "Complete Webelos Walkabout requirements (Outdoors)", "Required": True},

    # Elective Adventures (Complete any 2)
    {"Req_ID": "Aquanaut.1", "Adventure": "Aquanaut", "Requirement_Description": "Complete Aquanaut requirements", "Required": False},
    {"Req_ID": "ArtExplosion.1", "Adventure": "Art Explosion", "Requirement_Description": "Complete Art Explosion requirements", "Required": False},
    {"Req_ID": "AwareAndCare.1", "Adventure": "Aware and Care", "Requirement_Description": "Complete Aware and Care requirements", "Required": False},
    {"Req_ID": "BuildIt.1", "Adventure": "Build It", "Requirement_Description": "Complete Build It requirements", "Required": False},
    {"Req_ID": "CatchTheBigOne.1", "Adventure": "Catch the Big One", "Requirement_Description": "Complete Catch the Big One requirements", "Required": False},
    {"Req_ID": "ChampionsNatureWebelos.1", "Adventure": "Champions for Nature Webelos", "Requirement_Description": "Complete Champions for Nature Webelos requirements", "Required": False},
    {"Req_ID": "ChefsKnife.1", "Adventure": "Chef's Knife", "Requirement_Description": "Complete Chef's Knife requirements", "Required": False},
    {"Req_ID": "EarthRocks.1", "Adventure": "Earth Rocks", "Requirement_Description": "Complete Earth Rocks requirements", "Required": False},
    {"Req_ID": "LetsCampWebelos.1", "Adventure": "Let's Camp Webelos", "Requirement_Description": "Complete Let's Camp Webelos requirements", "Required": False},
    {"Req_ID": "MathOnTheTrail.1", "Adventure": "Math on the Trail", "Requirement_Description": "Complete Math on the Trail requirements", "Required": False},
    {"Req_ID": "ModularDesign.1", "Adventure": "Modular Design", "Requirement_Description": "Complete Modular Design requirements", "Required": False},
    {"Req_ID": "PaddleOnward.1", "Adventure": "Paddle Onward", "Requirement_Description": "Complete Paddle Onward requirements", "Required": False},
    {"Req_ID": "PedalAway.1", "Adventure": "Pedal Away", "Requirement_Description": "Complete Pedal Away requirements", "Required": False},
    {"Req_ID": "RaceTimeWebelos.1", "Adventure": "Race Time Webelos", "Requirement_Description": "Complete Race Time Webelos requirements", "Required": False},
    {"Req_ID": "SummertimeFunWebelos.1", "Adventure": "Summertime Fun Webelos", "Requirement_Description": "Complete Summertime Fun Webelos requirements", "Required": False},
    {"Req_ID": "TechOnTheTrail.1", "Adventure": "Tech on the Trail", "Requirement_Description": "Complete Tech on the Trail requirements", "Required": False},
    {"Req_ID": "YoYo.1", "Adventure": "Yo-yo", "Requirement_Description": "Complete Yo-yo requirements", "Required": False},
]

# Dictionary mapping rank names to their requirement sets
RANK_REQUIREMENTS = {
    "Lion (Kindergarten)": LION_REQUIREMENTS,
    "Tiger (1st Grade)": TIGER_REQUIREMENTS,
    "Wolf (2nd Grade)": WOLF_REQUIREMENTS,
    "Bear (3rd Grade)": BEAR_REQUIREMENTS,
    "Webelos (4th Grade)": WEBELOS_REQUIREMENTS,
}

# ============================================================================
# DATA INITIALIZATION FUNCTIONS
# ============================================================================

def initialize_data_files():
    """Create the data directory and initialize all CSV files if they don't exist."""

    # Create data directory
    DATA_DIR.mkdir(exist_ok=True)

    # Initialize Roster.csv
    if not ROSTER_FILE.exists():
        df = pd.DataFrame(columns=["Scout Name"])
        df.to_csv(ROSTER_FILE, index=False)

    # Initialize Requirement_Key.csv with default BSA requirements
    # This file can be edited by users through the "Manage Requirements" page
    if not REQUIREMENT_KEY_FILE.exists():
        df = pd.DataFrame(LION_REQUIREMENTS)
        df.to_csv(REQUIREMENT_KEY_FILE, index=False)

    # Initialize Meetings.csv
    if not MEETINGS_FILE.exists():
        df = pd.DataFrame(columns=["Meeting_Date", "Meeting_Title", "Req_IDs_Covered"])
        df.to_csv(MEETINGS_FILE, index=False)

    # Initialize Meeting_Attendance.csv
    if not ATTENDANCE_FILE.exists():
        df = pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])
        df.to_csv(ATTENDANCE_FILE, index=False)

# ============================================================================
# HELPER FUNCTIONS WITH CACHING
# ============================================================================

@st.cache_data
def load_roster():
    """Load the roster CSV file."""
    if ROSTER_FILE.exists():
        df = pd.read_csv(ROSTER_FILE)
        return df
    return pd.DataFrame(columns=["Scout Name"])

@st.cache_data
def load_requirement_key():
    """Load the requirement key CSV file."""
    if REQUIREMENT_KEY_FILE.exists():
        df = pd.read_csv(REQUIREMENT_KEY_FILE)
        return df
    return pd.DataFrame(columns=["Req_ID", "Adventure", "Requirement_Description", "Required"])

@st.cache_data
def load_meetings():
    """Load the meetings CSV file."""
    if MEETINGS_FILE.exists():
        df = pd.read_csv(MEETINGS_FILE)
        if not df.empty:
            df["Meeting_Date"] = pd.to_datetime(df["Meeting_Date"])
        return df
    return pd.DataFrame(columns=["Meeting_Date", "Meeting_Title", "Req_IDs_Covered"])

@st.cache_data
def load_attendance():
    """Load the attendance CSV file."""
    if ATTENDANCE_FILE.exists():
        df = pd.read_csv(ATTENDANCE_FILE)
        if not df.empty:
            df["Meeting_Date"] = pd.to_datetime(df["Meeting_Date"])
        return df
    return pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])

def clear_cache():
    """Clear all cached data after modifications."""
    load_roster.clear()
    load_requirement_key.clear()
    load_meetings.clear()
    load_attendance.clear()

def save_roster(df):
    """Save the roster dataframe to CSV."""
    df.to_csv(ROSTER_FILE, index=False)
    clear_cache()

def save_requirements(df):
    """Save the requirements dataframe to CSV."""
    df.to_csv(REQUIREMENT_KEY_FILE, index=False)
    clear_cache()

def save_meetings(df):
    """Save the meetings dataframe to CSV."""
    df_to_save = df.copy()
    if not df_to_save.empty:
        df_to_save["Meeting_Date"] = df_to_save["Meeting_Date"].dt.strftime("%Y-%m-%d")
    df_to_save.to_csv(MEETINGS_FILE, index=False)
    clear_cache()

def save_attendance(df):
    """Save the attendance dataframe to CSV."""
    df_to_save = df.copy()
    if not df_to_save.empty:
        df_to_save["Meeting_Date"] = df_to_save["Meeting_Date"].dt.strftime("%Y-%m-%d")
    df_to_save.to_csv(ATTENDANCE_FILE, index=False)
    clear_cache()

# ============================================================================
# PAGE 1: MANAGE ROSTER
# ============================================================================

def page_manage_roster():
    """Page for managing the den roster."""
    st.title("📋 Manage Roster")
    st.write("Add or remove scouts from your den's roster.")

    # Load current roster
    roster_df = load_roster()

    # Two column layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Add Scouts")

        # Create tabs for single vs bulk add
        tab1, tab2 = st.tabs(["Add One Scout", "Bulk Import"])

        # TAB 1: Single Scout Add
        with tab1:
            with st.form("add_scout_form"):
                new_scout_name = st.text_input("Scout Name", key="new_scout_name")
                submit_add = st.form_submit_button("Add Scout")

                if submit_add:
                    if not new_scout_name.strip():
                        st.error("❌ Please enter a scout name.")
                    elif new_scout_name in roster_df["Scout Name"].values:
                        st.error(f"❌ Scout '{new_scout_name}' already exists in the roster.")
                    else:
                        # Add new scout
                        new_row = pd.DataFrame({"Scout Name": [new_scout_name]})
                        roster_df = pd.concat([roster_df, new_row], ignore_index=True)
                        save_roster(roster_df)
                        st.success(f"✅ Added {new_scout_name} to the roster!")
                        st.rerun()

        # TAB 2: Bulk Import
        with tab2:
            with st.form("bulk_add_form"):
                st.write("Paste scout names below, one per line:")
                bulk_names = st.text_area(
                    "Scout Names",
                    height=200,
                    placeholder="John Smith\nJane Doe\nBob Johnson\n...",
                    key="bulk_scout_names",
                    help="Enter or paste multiple scout names, one per line"
                )
                submit_bulk = st.form_submit_button("Add All Scouts")

                if submit_bulk:
                    if not bulk_names.strip():
                        st.error("❌ Please enter at least one scout name.")
                    else:
                        # Parse the input - split by newlines and clean up
                        scout_names = [name.strip() for name in bulk_names.split('\n') if name.strip()]

                        if not scout_names:
                            st.error("❌ No valid scout names found.")
                        else:
                            # Filter out duplicates and existing scouts
                            existing_scouts = set(roster_df["Scout Name"].values)
                            new_scouts = []
                            skipped_duplicates = []
                            skipped_existing = []

                            for name in scout_names:
                                if name in existing_scouts:
                                    skipped_existing.append(name)
                                elif name in new_scouts:
                                    skipped_duplicates.append(name)
                                else:
                                    new_scouts.append(name)
                                    existing_scouts.add(name)  # Track for duplicate detection

                            # Add new scouts
                            if new_scouts:
                                new_rows = pd.DataFrame({"Scout Name": new_scouts})
                                roster_df = pd.concat([roster_df, new_rows], ignore_index=True)
                                save_roster(roster_df)
                                st.success(f"✅ Added {len(new_scouts)} scout(s) to the roster!")

                                # Show warnings if any were skipped
                                if skipped_existing:
                                    st.warning(f"⚠️ Skipped {len(skipped_existing)} scout(s) already in roster: {', '.join(skipped_existing[:5])}{'...' if len(skipped_existing) > 5 else ''}")
                                if skipped_duplicates:
                                    st.warning(f"⚠️ Removed {len(skipped_duplicates)} duplicate(s) from input: {', '.join(skipped_duplicates[:5])}{'...' if len(skipped_duplicates) > 5 else ''}")

                                st.rerun()
                            else:
                                st.error("❌ No new scouts to add. All names are already in the roster.")

    with col2:
        st.subheader("Current Den Roster")
        if not roster_df.empty:
            st.dataframe(roster_df, use_container_width=True, hide_index=True)

            # Remove scout section
            st.write("---")
            scout_to_remove = st.selectbox(
                "Select a scout to remove:",
                options=roster_df["Scout Name"].tolist(),
                key="scout_to_remove"
            )
            if st.button("Remove Selected Scout"):
                roster_df = roster_df[roster_df["Scout Name"] != scout_to_remove]
                save_roster(roster_df)
                st.success(f"✅ Removed {scout_to_remove} from the roster!")
                st.rerun()
        else:
            st.info("No scouts in the roster yet. Add some scouts to get started!")

# ============================================================================
# PAGE 2: MANAGE REQUIREMENTS
# ============================================================================

def page_manage_requirements():
    """Page for managing adventure requirements (CRUD operations)."""
    st.title("📚 Manage Requirements")
    st.write("Add, edit, or remove adventure requirements for your den.")

    # Load current requirements
    requirements_df = load_requirement_key()

    # Create tabs for different operations
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["View All", "Add New", "Edit Existing", "Delete", "Import/Export"])

    # TAB 1: View All Requirements
    with tab1:
        st.subheader("All Requirements")
        if not requirements_df.empty:
            # Group by required/elective first
            st.write("### Required Adventures (Must complete all)")
            required_df = requirements_df[requirements_df["Required"] == True]
            if not required_df.empty:
                adventures = required_df["Adventure"].unique()
                for adventure in sorted(adventures):
                    with st.expander(f"{adventure} ({len(required_df[required_df['Adventure'] == adventure])} requirements)"):
                        adventure_reqs = required_df[required_df["Adventure"] == adventure]
                        st.dataframe(adventure_reqs, use_container_width=True, hide_index=True)
            else:
                st.info("No required adventures found.")

            st.write("---")
            st.write("### Elective Adventures (Must complete any 2)")
            elective_df = requirements_df[requirements_df["Required"] == False]
            if not elective_df.empty:
                adventures = elective_df["Adventure"].unique()
                for adventure in sorted(adventures):
                    with st.expander(f"{adventure} ({len(elective_df[elective_df['Adventure'] == adventure])} requirements)"):
                        adventure_reqs = elective_df[elective_df["Adventure"] == adventure]
                        st.dataframe(adventure_reqs, use_container_width=True, hide_index=True)
            else:
                st.info("No elective adventures found.")
        else:
            st.info("No requirements found. Add some requirements to get started!")

    # TAB 2: Add New Requirement
    with tab2:
        st.subheader("Add a New Requirement")
        with st.form("add_requirement_form"):
            new_req_id = st.text_input(
                "Requirement ID",
                placeholder="e.g., Bobcat.1 or MyAdventure.1",
                help="Use format: AdventureName.Number"
            )
            new_adventure = st.text_input(
                "Adventure Name",
                placeholder="e.g., Bobcat, Fun on the Run",
                help="Name of the adventure this requirement belongs to"
            )
            new_description = st.text_area(
                "Requirement Description",
                placeholder="e.g., 1. Get to know the members of your den",
                help="Detailed description of what scouts need to do"
            )
            new_required = st.checkbox(
                "Required Adventure",
                value=False,
                help="Check if this is a required adventure (must complete all required adventures). Uncheck for elective adventures (must complete any 2)."
            )

            submit_add = st.form_submit_button("Add Requirement")

            if submit_add:
                if not new_req_id.strip() or not new_adventure.strip() or not new_description.strip():
                    st.error("❌ Please fill in all fields.")
                elif new_req_id in requirements_df["Req_ID"].values:
                    st.error(f"❌ Requirement ID '{new_req_id}' already exists.")
                else:
                    # Add new requirement
                    new_row = pd.DataFrame({
                        "Req_ID": [new_req_id],
                        "Adventure": [new_adventure],
                        "Requirement_Description": [new_description],
                        "Required": [new_required]
                    })
                    requirements_df = pd.concat([requirements_df, new_row], ignore_index=True)
                    save_requirements(requirements_df)
                    st.success(f"✅ Added requirement {new_req_id}!")
                    st.rerun()

    # TAB 3: Edit Existing Requirement
    with tab3:
        st.subheader("Edit an Existing Requirement")
        if not requirements_df.empty:
            # Select requirement to edit
            req_options = [
                f"{row['Req_ID']} - {row['Requirement_Description'][:50]}..."
                for _, row in requirements_df.iterrows()
            ]
            selected_req = st.selectbox(
                "Select a requirement to edit:",
                options=req_options,
                key="edit_req_select"
            )

            if selected_req:
                # Extract Req_ID from selection
                selected_req_id = selected_req.split(" - ")[0]
                current_req = requirements_df[requirements_df["Req_ID"] == selected_req_id].iloc[0]

                with st.form("edit_requirement_form"):
                    st.write(f"Editing: **{selected_req_id}**")

                    edit_adventure = st.text_input(
                        "Adventure Name",
                        value=current_req["Adventure"]
                    )
                    edit_description = st.text_area(
                        "Requirement Description",
                        value=current_req["Requirement_Description"],
                        height=100
                    )
                    edit_required = st.checkbox(
                        "Required Adventure",
                        value=bool(current_req["Required"]),
                        help="Check if this is a required adventure (must complete all required adventures). Uncheck for elective adventures (must complete any 2)."
                    )

                    submit_edit = st.form_submit_button("Save Changes")

                    if submit_edit:
                        # Update the requirement
                        requirements_df.loc[
                            requirements_df["Req_ID"] == selected_req_id,
                            ["Adventure", "Requirement_Description", "Required"]
                        ] = [edit_adventure, edit_description, edit_required]
                        save_requirements(requirements_df)
                        st.success(f"✅ Updated requirement {selected_req_id}!")
                        st.rerun()
        else:
            st.info("No requirements available to edit.")

    # TAB 4: Delete Requirement
    with tab4:
        st.subheader("Delete a Requirement")
        if not requirements_df.empty:
            req_to_delete = st.selectbox(
                "Select a requirement to delete:",
                options=requirements_df["Req_ID"].tolist(),
                key="delete_req_select"
            )

            if req_to_delete:
                req_details = requirements_df[requirements_df["Req_ID"] == req_to_delete].iloc[0]
                st.warning(f"**Warning:** You are about to delete:")
                st.write(f"- **ID:** {req_details['Req_ID']}")
                st.write(f"- **Adventure:** {req_details['Adventure']}")
                st.write(f"- **Description:** {req_details['Requirement_Description']}")

                if st.button("⚠️ Confirm Delete", type="primary"):
                    requirements_df = requirements_df[requirements_df["Req_ID"] != req_to_delete]
                    save_requirements(requirements_df)
                    st.success(f"✅ Deleted requirement {req_to_delete}!")
                    st.rerun()
        else:
            st.info("No requirements available to delete.")

    # TAB 5: Import/Export
    with tab5:
        st.subheader("Import/Export Requirements")
        st.write("Share requirements with other dens or back up your customizations.")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### 📥 Import Requirements")
            st.write("Upload a CSV file with requirements to replace or add to your current set.")

            uploaded_file = st.file_uploader(
                "Choose a CSV file",
                type="csv",
                key="import_requirements",
                help="CSV must have columns: Req_ID, Adventure, Requirement_Description, Required"
            )

            import_mode = st.radio(
                "Import Mode:",
                ["Replace All (clear existing)", "Add New (keep existing)"],
                key="import_mode"
            )

            if uploaded_file is not None:
                try:
                    imported_df = pd.read_csv(uploaded_file)

                    # Validate required columns
                    required_cols = ["Req_ID", "Adventure", "Requirement_Description", "Required"]
                    if not all(col in imported_df.columns for col in required_cols):
                        st.error(f"❌ CSV must contain columns: {', '.join(required_cols)}")
                    else:
                        st.write(f"**Preview:** {len(imported_df)} requirements found")
                        st.dataframe(imported_df.head(), use_container_width=True)

                        if st.button("✅ Import Requirements", type="primary"):
                            if import_mode == "Replace All (clear existing)":
                                save_requirements(imported_df)
                                st.success(f"✅ Replaced all requirements with {len(imported_df)} imported requirements!")
                            else:
                                # Add new, skip duplicates
                                existing_ids = set(requirements_df["Req_ID"].values)
                                new_reqs = imported_df[~imported_df["Req_ID"].isin(existing_ids)]
                                if not new_reqs.empty:
                                    combined_df = pd.concat([requirements_df, new_reqs], ignore_index=True)
                                    save_requirements(combined_df)
                                    st.success(f"✅ Added {len(new_reqs)} new requirements!")
                                else:
                                    st.warning("⚠️ No new requirements to add (all IDs already exist)")
                            st.rerun()

                except Exception as e:
                    st.error(f"❌ Error reading CSV: {str(e)}")

        with col2:
            st.write("### 📤 Export Requirements")
            st.write("Download your current requirements as a CSV file to share or back up.")

            if not requirements_df.empty:
                # Convert DataFrame to CSV
                csv = requirements_df.to_csv(index=False)

                st.download_button(
                    label="⬇️ Download Requirements CSV",
                    data=csv,
                    file_name="scout_requirements.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.info(f"📊 {len(requirements_df)} requirements ready to export")
            else:
                st.warning("No requirements to export")

        st.write("---")

        # Load Pre-Packaged Requirements
        st.write("### 📦 Load Pre-Packaged Requirements")
        st.write("Quickly switch to a different Cub Scout rank with official BSA adventure structure.")

        selected_rank = st.selectbox(
            "Select Rank:",
            options=list(RANK_REQUIREMENTS.keys()),
            key="rank_selector",
            help="Choose a rank to load its pre-packaged requirements"
        )

        if selected_rank:
            rank_reqs = RANK_REQUIREMENTS[selected_rank]
            required_count = sum(1 for r in rank_reqs if r["Required"])
            elective_count = sum(1 for r in rank_reqs if not r["Required"])

            st.info(f"**{selected_rank}** has {required_count} required adventures and {elective_count} elective adventures")

            if st.button(f"📥 Load {selected_rank} Requirements", type="primary", use_container_width=True):
                if st.session_state.get("confirm_load_rank", False):
                    df = pd.DataFrame(rank_reqs)
                    save_requirements(df)
                    st.session_state["confirm_load_rank"] = False
                    st.success(f"✅ Loaded {selected_rank} requirements!")
                    st.rerun()
                else:
                    st.session_state["confirm_load_rank"] = True
                    st.warning(f"⚠️ Click again to confirm. This will replace ALL current requirements with {selected_rank} requirements!")

        st.write("---")

        # Quick Actions
        st.write("### ⚙️ Quick Actions")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Reset to Lion Scout Defaults", use_container_width=True):
                if st.session_state.get("confirm_reset", False):
                    # Reload the default Lion requirements
                    df = pd.DataFrame(LION_REQUIREMENTS)
                    save_requirements(df)
                    st.session_state["confirm_reset"] = False
                    st.success("✅ Reset to Lion Scout defaults!")
                    st.rerun()
                else:
                    st.session_state["confirm_reset"] = True
                    st.warning("⚠️ Click again to confirm reset. This will replace ALL current requirements!")

        with col2:
            if st.button("🗑️ Clear All Requirements", use_container_width=True):
                if st.session_state.get("confirm_clear", False):
                    empty_df = pd.DataFrame(columns=["Req_ID", "Adventure", "Requirement_Description", "Required"])
                    save_requirements(empty_df)
                    st.session_state["confirm_clear"] = False
                    st.success("✅ All requirements cleared!")
                    st.rerun()
                else:
                    st.session_state["confirm_clear"] = True
                    st.warning("⚠️ Click again to confirm clear. This cannot be undone!")

# ============================================================================
# PAGE 3: MANAGE MEETINGS
# ============================================================================

def page_manage_meetings():
    """Page for creating and managing den meetings."""
    st.title("📅 Manage Meetings")
    st.write("Define each meeting by its date, title, and requirements covered.")

    # Load data
    requirement_key = load_requirement_key()
    meetings_df = load_meetings()

    # Create formatted options for multiselect
    requirement_options = [
        f"{row['Req_ID']} - {row['Requirement_Description']}"
        for _, row in requirement_key.iterrows()
    ]

    # Add meeting form
    st.subheader("Add a New Meeting")
    with st.form("add_meeting_form"):
        meeting_date = st.date_input("Meeting Date", key="meeting_date")
        meeting_title = st.text_input("Meeting Title", key="meeting_title")
        selected_requirements = st.multiselect(
            "Requirements Covered",
            options=requirement_options,
            key="selected_requirements"
        )

        submit_meeting = st.form_submit_button("Add Meeting")

        if submit_meeting:
            if not meeting_title.strip():
                st.error("❌ Please enter a meeting title.")
            elif not selected_requirements:
                st.error("❌ Please select at least one requirement.")
            elif not meetings_df.empty and meeting_date in meetings_df["Meeting_Date"].dt.date.values:
                st.error(f"❌ A meeting already exists for {meeting_date}. Please choose a different date.")
            else:
                # Extract Req_IDs from selected options
                req_ids = [req.split(" - ")[0] for req in selected_requirements]
                req_ids_str = ",".join(req_ids)

                # Add new meeting
                new_meeting = pd.DataFrame({
                    "Meeting_Date": [pd.to_datetime(meeting_date)],
                    "Meeting_Title": [meeting_title],
                    "Req_IDs_Covered": [req_ids_str]
                })
                meetings_df = pd.concat([meetings_df, new_meeting], ignore_index=True)
                save_meetings(meetings_df)
                st.success(f"✅ Added meeting '{meeting_title}' for {meeting_date}!")
                st.rerun()

    # Display existing meetings
    st.write("---")
    st.subheader("Existing Meetings")
    if not meetings_df.empty:
        # Sort by date descending
        display_df = meetings_df.sort_values("Meeting_Date", ascending=False).copy()
        display_df["Meeting_Date"] = display_df["Meeting_Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No meetings scheduled yet. Add a meeting above to get started!")

# ============================================================================
# PAGE 4: LOG MEETING ATTENDANCE
# ============================================================================

def page_log_attendance():
    """Page for logging which scouts attended each meeting."""
    st.title("✅ Log Meeting Attendance")
    st.write("Select a meeting to record or edit attendance.")

    # Load data
    roster_df = load_roster()
    meetings_df = load_meetings()
    attendance_df = load_attendance()

    if meetings_df.empty:
        st.warning("⚠️ No meetings have been created yet. Please add meetings in the 'Manage Meetings' page first.")
        return

    if roster_df.empty:
        st.warning("⚠️ No scouts in the roster yet. Please add scouts in the 'Manage Roster' page first.")
        return

    # Create meeting selection options
    meeting_options = [
        f"{row['Meeting_Date'].strftime('%Y-%m-%d')} - {row['Meeting_Title']}"
        for _, row in meetings_df.iterrows()
    ]
    meeting_dates = meetings_df["Meeting_Date"].tolist()

    selected_meeting_str = st.selectbox(
        "Select a Meeting",
        options=meeting_options,
        key="selected_meeting"
    )

    # Get the selected meeting date
    selected_idx = meeting_options.index(selected_meeting_str)
    selected_date = meeting_dates[selected_idx]

    # Get current attendance for this meeting
    current_attendees = attendance_df[
        attendance_df["Meeting_Date"] == selected_date
    ]["Scout_Name"].tolist()

    # Show attendance status
    total_scouts = len(roster_df)
    attendance_count = len(current_attendees)

    st.write("---")

    # Show current attendance first
    st.subheader("📊 Current Attendance")

    if current_attendees:
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Present ({len(current_attendees)}):**")
            for scout in sorted(current_attendees):
                st.write(f"✅ {scout}")

        with col2:
            # Show who was absent
            absent_scouts = [scout for scout in roster_df["Scout Name"] if scout not in current_attendees]
            if absent_scouts:
                st.write(f"**Absent ({len(absent_scouts)}):**")
                for scout in sorted(absent_scouts):
                    st.write(f"❌ {scout}")
            else:
                st.success("🎉 Perfect attendance!")

        st.info(f"**Summary:** {attendance_count} of {total_scouts} scouts attended ({(attendance_count/total_scouts*100):.0f}%)")
    else:
        st.warning("⚠️ No attendance recorded yet for this meeting")

    st.write("---")

    # Attendance form for editing
    st.subheader("✏️ Edit Attendance")
    st.write("Modify the selections below and click Save to update attendance.")

    # Use the meeting date as part of the form key to force re-render when meeting changes
    form_key = f"attendance_form_{selected_date.strftime('%Y%m%d')}"

    with st.form(form_key):
        selected_scouts = st.multiselect(
            "Scouts who were Present",
            options=roster_df["Scout Name"].tolist(),
            default=current_attendees,
            help="Select all scouts who attended this meeting"
        )

        col1, col2 = st.columns([1, 3])
        with col1:
            submit_attendance = st.form_submit_button("💾 Save Attendance", use_container_width=True)
        with col2:
            st.write(f"*Selected: {len(selected_scouts)} of {total_scouts} scouts*")

        if submit_attendance:
            # Remove all existing attendance records for this date
            attendance_df = attendance_df[attendance_df["Meeting_Date"] != selected_date]

            # Add new attendance records
            if selected_scouts:
                new_attendance = pd.DataFrame({
                    "Meeting_Date": [selected_date] * len(selected_scouts),
                    "Scout_Name": selected_scouts
                })
                attendance_df = pd.concat([attendance_df, new_attendance], ignore_index=True)

            save_attendance(attendance_df)

            if current_attendees:
                st.success(f"✅ Attendance updated for {selected_date.strftime('%Y-%m-%d')}! ({len(selected_scouts)} scouts)")
            else:
                st.success(f"✅ Attendance recorded for {selected_date.strftime('%Y-%m-%d')}! ({len(selected_scouts)} scouts)")
            st.rerun()

# ============================================================================
# PAGE 5: TRACKER DASHBOARD
# ============================================================================

def page_tracker_dashboard():
    """Dashboard showing advancement progress for all scouts."""
    st.title("📊 Tracker Dashboard")
    st.write("View progress for all scouts in your den.")

    # Load all data
    roster_df = load_roster()
    requirement_key = load_requirement_key()
    meetings_df = load_meetings()
    attendance_df = load_attendance()

    if roster_df.empty:
        st.warning("⚠️ No scouts in the roster yet. Please add scouts to get started!")
        return

    # Build master tracker DataFrame
    scouts = roster_df["Scout Name"].tolist()
    req_ids = requirement_key["Req_ID"].tolist()

    # Initialize with all False
    master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

    # Create lookup dictionary: Meeting_Date -> Req_IDs_Covered
    meeting_req_lookup = {}
    for _, meeting in meetings_df.iterrows():
        req_ids_covered = meeting["Req_IDs_Covered"].split(",") if pd.notna(meeting["Req_IDs_Covered"]) else []
        meeting_req_lookup[meeting["Meeting_Date"]] = req_ids_covered

    # Process attendance to mark completed requirements
    for _, attendance_row in attendance_df.iterrows():
        scout_name = attendance_row["Scout_Name"]
        meeting_date = attendance_row["Meeting_Date"]

        if scout_name in master_tracker.index and meeting_date in meeting_req_lookup:
            req_ids_covered = meeting_req_lookup[meeting_date]
            for req_id in req_ids_covered:
                if req_id in master_tracker.columns:
                    master_tracker.at[scout_name, req_id] = True

    # ========================================================================
    # SUMMARY VIEW
    # ========================================================================

    st.subheader("📈 Adventure Completion Summary")

    # Separate required and elective adventures
    required_adventures = requirement_key[requirement_key["Required"] == True]["Adventure"].unique()
    elective_adventures = requirement_key[requirement_key["Required"] == False]["Adventure"].unique()

    # Calculate completion data for all scouts
    required_summary_data = []
    elective_summary_data = []
    rank_completion_data = []

    for scout in scouts:
        # Required adventures
        required_summary = {"Scout Name": scout}
        all_required_complete = True

        for adventure in required_adventures:
            adventure_reqs = requirement_key[requirement_key["Adventure"] == adventure]["Req_ID"].tolist()
            completed = master_tracker.loc[scout, adventure_reqs].sum()
            total = len(adventure_reqs)
            percentage = (completed / total * 100) if total > 0 else 0  # Convert to 0-100 scale
            required_summary[adventure] = percentage
            if percentage < 100.0:
                all_required_complete = False

        required_summary_data.append(required_summary)

        # Elective adventures
        elective_summary = {"Scout Name": scout}
        completed_electives = 0

        for adventure in elective_adventures:
            adventure_reqs = requirement_key[requirement_key["Adventure"] == adventure]["Req_ID"].tolist()
            completed = master_tracker.loc[scout, adventure_reqs].sum()
            total = len(adventure_reqs)
            percentage = (completed / total * 100) if total > 0 else 0  # Convert to 0-100 scale
            elective_summary[adventure] = percentage
            if percentage == 100.0:
                completed_electives += 1

        elective_summary_data.append(elective_summary)

        # Lion Rank completion: All required + at least 2 electives
        lion_rank_earned = all_required_complete and completed_electives >= 2
        rank_completion_data.append({
            "Scout Name": scout,
            "Required Complete": "✅ Yes" if all_required_complete else "❌ No",
            "Electives Complete": f"{completed_electives} / 2",
            "Lion Rank Earned": "✅ Yes" if lion_rank_earned else "❌ No"
        })

    # Display Required Adventures Table
    st.write("### Required Adventures (Must complete all 6)")
    required_summary_df = pd.DataFrame(required_summary_data)

    required_column_config = {"Scout Name": st.column_config.TextColumn("Scout Name")}
    for adventure in required_adventures:
        required_column_config[adventure] = st.column_config.ProgressColumn(
            adventure,
            format="%.0f%%",
            min_value=0,
            max_value=100,
        )

    st.dataframe(
        required_summary_df,
        column_config=required_column_config,
        use_container_width=True,
        hide_index=True
    )

    st.write("---")

    # Display Elective Adventures Table
    st.write("### Elective Adventures (Must complete any 2)")
    elective_summary_df = pd.DataFrame(elective_summary_data)

    elective_column_config = {"Scout Name": st.column_config.TextColumn("Scout Name")}
    for adventure in elective_adventures:
        elective_column_config[adventure] = st.column_config.ProgressColumn(
            adventure,
            format="%.0f%%",
            min_value=0,
            max_value=100,
        )

    st.dataframe(
        elective_summary_df,
        column_config=elective_column_config,
        use_container_width=True,
        hide_index=True
    )

    st.write("---")

    # Display Lion Rank Completion Status
    st.write("### Lion Rank Completion Status")
    rank_completion_df = pd.DataFrame(rank_completion_data)
    st.dataframe(
        rank_completion_df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================================
    # DETAILED VIEW
    # ========================================================================

    with st.expander("🔍 Show Detailed Requirement Tracker"):
        st.write("Detailed view showing each requirement completion status.")

        # Create display version with checkmarks
        display_tracker = master_tracker.copy()
        display_tracker = display_tracker.replace({True: "✅", False: "❌"})

        st.dataframe(
            display_tracker,
            use_container_width=True
        )

# ============================================================================
# PAGE 6: PLAN MEETINGS
# ============================================================================

def page_plan_meetings():
    """Page for planning future meetings based on requirement completion."""
    st.title("📅 Plan Meetings")
    st.write("See which required requirements need the most attention to help plan your next meetings.")

    # Load all data
    roster_df = load_roster()
    requirement_key = load_requirement_key()
    meetings_df = load_meetings()
    attendance_df = load_attendance()

    if roster_df.empty:
        st.warning("⚠️ No scouts in the roster yet. Please add scouts to get started!")
        return

    # Build master tracker DataFrame
    scouts = roster_df["Scout Name"].tolist()
    req_ids = requirement_key["Req_ID"].tolist()

    # Initialize with all False
    master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

    # Create lookup dictionary: Meeting_Date -> Req_IDs_Covered
    meeting_req_lookup = {}
    for _, meeting in meetings_df.iterrows():
        req_ids_covered = meeting["Req_IDs_Covered"].split(",") if pd.notna(meeting["Req_IDs_Covered"]) else []
        meeting_req_lookup[meeting["Meeting_Date"]] = req_ids_covered

    # Process attendance to mark completed requirements
    for _, attendance_row in attendance_df.iterrows():
        scout_name = attendance_row["Scout_Name"]
        meeting_date = attendance_row["Meeting_Date"]

        if scout_name in master_tracker.index and meeting_date in meeting_req_lookup:
            req_ids_covered = meeting_req_lookup[meeting_date]
            for req_id in req_ids_covered:
                if req_id in master_tracker.columns:
                    master_tracker.at[scout_name, req_id] = True

    # Get only required requirements
    required_reqs = requirement_key[requirement_key["Required"] == True].copy()

    # Calculate completion statistics for each requirement
    planning_data = []

    for _, req_row in required_reqs.iterrows():
        req_id = req_row["Req_ID"]
        adventure = req_row["Adventure"]
        description = req_row["Requirement_Description"]

        # Count how many scouts have completed this requirement
        completed_count = master_tracker[req_id].sum()
        total_scouts = len(scouts)
        completion_percentage = (completed_count / total_scouts * 100) if total_scouts > 0 else 0

        # Get list of scouts who haven't completed it
        scouts_missing = [scout for scout in scouts if not master_tracker.loc[scout, req_id]]

        planning_data.append({
            "Req_ID": req_id,
            "Adventure": adventure,
            "Requirement": description,
            "Completed": completed_count,
            "Total Scouts": total_scouts,
            "% Complete": completion_percentage,
            "Scouts Missing": ", ".join(scouts_missing) if scouts_missing else "All complete!"
        })

    planning_df = pd.DataFrame(planning_data)

    # Sort by completion percentage (lowest first) to show most needed requirements at top
    planning_df = planning_df.sort_values("% Complete", ascending=True)

    # Display options
    st.subheader("View Options")
    col1, col2 = st.columns(2)

    with col1:
        view_mode = st.radio(
            "Show:",
            ["All Required Requirements", "Incomplete Only (< 100%)", "Most Needed (< 50%)"],
            key="view_mode"
        )

    with col2:
        group_by_adventure = st.checkbox("Group by Adventure", value=True)

    # Filter based on view mode
    if view_mode == "Incomplete Only (< 100%)":
        filtered_df = planning_df[planning_df["% Complete"] < 100]
    elif view_mode == "Most Needed (< 50%)":
        filtered_df = planning_df[planning_df["% Complete"] < 50]
    else:
        filtered_df = planning_df

    if filtered_df.empty:
        st.success("🎉 All scouts have completed all required requirements!")
        return

    st.write("---")

    # Display the data
    if group_by_adventure:
        st.subheader("Required Requirements by Adventure")
        adventures = filtered_df["Adventure"].unique()

        for adventure in adventures:
            adventure_reqs = filtered_df[filtered_df["Adventure"] == adventure]

            # Calculate adventure-level stats
            avg_completion = adventure_reqs["% Complete"].mean()

            with st.expander(f"**{adventure}** ({len(adventure_reqs)} requirements, {avg_completion:.0f}% average completion)", expanded=True):
                for _, req_row in adventure_reqs.iterrows():
                    completion = req_row["% Complete"]

                    # Color-code based on completion
                    if completion == 100:
                        status_color = "🟢"
                    elif completion >= 50:
                        status_color = "🟡"
                    else:
                        status_color = "🔴"

                    st.write(f"{status_color} **{req_row['Req_ID']}** ({completion:.0f}% complete)")
                    st.write(f"   *{req_row['Requirement']}*")
                    st.write(f"   **Completed by:** {req_row['Completed']} of {req_row['Total Scouts']} scouts")

                    if req_row['Scouts Missing'] != "All complete!":
                        st.write(f"   **Still need:** {req_row['Scouts Missing']}")
                    st.write("")
    else:
        st.subheader("All Required Requirements")

        # Configure column display
        column_config = {
            "Req_ID": st.column_config.TextColumn("Requirement ID", width="small"),
            "Adventure": st.column_config.TextColumn("Adventure", width="medium"),
            "Requirement": st.column_config.TextColumn("Requirement", width="large"),
            "Completed": st.column_config.NumberColumn("Completed", width="small"),
            "Total Scouts": st.column_config.NumberColumn("Total", width="small"),
            "% Complete": st.column_config.ProgressColumn(
                "% Complete",
                format="%.0f%%",
                min_value=0,
                max_value=100,
                width="small"
            ),
            "Scouts Missing": st.column_config.TextColumn("Scouts Missing", width="large")
        }

        st.dataframe(
            filtered_df,
            column_config=column_config,
            use_container_width=True,
            hide_index=True
        )

    # Summary statistics
    st.write("---")
    st.subheader("📊 Summary Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_reqs = len(required_reqs)
        completed_reqs = len(planning_df[planning_df["% Complete"] == 100])
        st.metric("Required Requirements", f"{completed_reqs} / {total_reqs} at 100%")

    with col2:
        avg_completion = planning_df["% Complete"].mean()
        st.metric("Average Completion", f"{avg_completion:.0f}%")

    with col3:
        needs_attention = len(planning_df[planning_df["% Complete"] < 50])
        st.metric("Needs Most Attention", f"{needs_attention} requirements")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""

    # Initialize data files on first run
    initialize_data_files()

    # Configure page
    st.set_page_config(
        page_title="Lion Scout Tracker",
        page_icon="🦁",
        layout="wide"
    )

    # Sidebar navigation
    st.sidebar.title("🦁 Lion Scout Tracker")
    st.sidebar.write("---")

    page = st.sidebar.radio(
        "Navigation",
        ["Manage Roster", "Manage Requirements", "Plan Meetings", "Manage Meetings", "Log Attendance", "Tracker Dashboard"],
        key="navigation"
    )

    st.sidebar.write("---")
    st.sidebar.info(
        "**Workflow:**\n"
        "1. Add scouts to roster\n"
        "2. Configure requirements\n"
        "3. Plan & create meetings\n"
        "4. Log attendance\n"
        "5. View progress"
    )

    # Route to selected page
    if page == "Manage Roster":
        page_manage_roster()
    elif page == "Manage Requirements":
        page_manage_requirements()
    elif page == "Plan Meetings":
        page_plan_meetings()
    elif page == "Manage Meetings":
        page_manage_meetings()
    elif page == "Log Attendance":
        page_log_attendance()
    elif page == "Tracker Dashboard":
        page_tracker_dashboard()

if __name__ == "__main__":
    main()
