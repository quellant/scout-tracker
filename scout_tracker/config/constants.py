"""
Scout Tracker Constants and Configuration

This module contains all static configuration data and rank requirements
for the Scout Tracker application, including:
- File paths and directories
- BSA Cub Scout rank requirements for all ranks (Lion through Webelos)
"""

from pathlib import Path

# ============================================================================
# FILE PATHS AND CONFIGURATION
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
    # Bobcat Tiger (6 requirements)
    {"Req_ID": "BobcatTiger.1", "Adventure": "Bobcat Tiger", "Requirement_Description": "Get to know members of your den.", "Required": True},
    {"Req_ID": "BobcatTiger.2", "Adventure": "Bobcat Tiger", "Requirement_Description": "Recite the Scout Oath and Law with your den and den leader.", "Required": True},
    {"Req_ID": "BobcatTiger.3", "Adventure": "Bobcat Tiger", "Requirement_Description": "Learn about the Scout Oath. Identify the three parts of the Scout Oath.", "Required": True},
    {"Req_ID": "BobcatTiger.4", "Adventure": "Bobcat Tiger", "Requirement_Description": "With your den create a den Code of Conduct.", "Required": True},
    {"Req_ID": "BobcatTiger.5", "Adventure": "Bobcat Tiger", "Requirement_Description": "Demonstrate the Cub Scout sign, Cub Scout salute, and Cub Scout handshake. Show how each is used.", "Required": True},
    {"Req_ID": "BobcatTiger.6", "Adventure": "Bobcat Tiger", "Requirement_Description": "At home, with your parent or legal guardian do the activities in the booklet 'How to Protect Your Children from Child Abuse: A Parent's Guide.'", "Required": True},

    # Tiger Bites (4 requirements)
    {"Req_ID": "TigerBites.1", "Adventure": "Tiger Bites", "Requirement_Description": "Identify three foods that you can eat for a meal or snack from each of the following food groups: protein, vegetables, fruits, dairy, and grains.", "Required": True},
    {"Req_ID": "TigerBites.2", "Adventure": "Tiger Bites", "Requirement_Description": "Be active for 30 minutes with your den or at least one other person in a way that includes stretching and moving.", "Required": True},
    {"Req_ID": "TigerBites.3", "Adventure": "Tiger Bites", "Requirement_Description": "Be active for 10 minutes doing personal exercises that include cardio, muscular strength, and flexibility.", "Required": True},
    {"Req_ID": "TigerBites.4", "Adventure": "Tiger Bites", "Requirement_Description": "Do a relaxing activity for 10 minutes.", "Required": True},

    # Tiger's Roar (4 requirements)
    {"Req_ID": "TigersRoar.1", "Adventure": "Tiger's Roar", "Requirement_Description": "With permission from your parent or legal guardian, watch the Protect Yourself Rules video for the Tiger rank.", "Required": True},
    {"Req_ID": "TigersRoar.2", "Adventure": "Tiger's Roar", "Requirement_Description": "Complete the Personal Space Bubble worksheet that is part of the Protect Yourself Rules resources.", "Required": True},
    {"Req_ID": "TigersRoar.3", "Adventure": "Tiger's Roar", "Requirement_Description": "Discuss what to do if you become separated from your adult partner or group while in public.", "Required": True},
    {"Req_ID": "TigersRoar.4", "Adventure": "Tiger's Roar", "Requirement_Description": "Share what to do if you encounter a dangerous or uncomfortable situation.", "Required": True},

    # Tiger Circles (3 requirements)
    {"Req_ID": "TigerCircles.1", "Adventure": "Tiger Circles", "Requirement_Description": "Gather the items you need for a circle with an adult partner or other family members. Then, with your family, make a circle.", "Required": True},
    {"Req_ID": "TigerCircles.2", "Adventure": "Tiger Circles", "Requirement_Description": "With your adult partner or other family members, discover one of the reasons people gather in a circle to discuss faith.", "Required": True},
    {"Req_ID": "TigerCircles.3", "Adventure": "Tiger Circles", "Requirement_Description": "With your family, do an act of kindness or service for someone.", "Required": True},

    # Team Tiger (4 requirements)
    {"Req_ID": "TeamTiger.1", "Adventure": "Team Tiger", "Requirement_Description": "With your den, discuss the history and meaning of the United States flag. Demonstrate how to properly display the flag, and how to fold it.", "Required": True},
    {"Req_ID": "TeamTiger.2", "Adventure": "Team Tiger", "Requirement_Description": "Participate in a flag ceremony.", "Required": True},
    {"Req_ID": "TeamTiger.3", "Adventure": "Team Tiger", "Requirement_Description": "Learn about someone's job and what they do to help others.", "Required": True},
    {"Req_ID": "TeamTiger.4", "Adventure": "Team Tiger", "Requirement_Description": "With your den or family, do something to help the people in your local community or find out about organizations that help others.", "Required": True},

    # Tigers in the Wild (5 requirements)
    {"Req_ID": "TigersInTheWild.1", "Adventure": "Tigers in the Wild", "Requirement_Description": "With your den, identify what you need for a 1-mile walk outside. Gather your Cub Scout Six Essentials and weather appropriate clothing and shoes.", "Required": True},
    {"Req_ID": "TigersInTheWild.2", "Adventure": "Tigers in the Wild", "Requirement_Description": "Learn what SAW (Stay, Answer, Whistle) means.", "Required": True},
    {"Req_ID": "TigersInTheWild.3", "Adventure": "Tigers in the Wild", "Requirement_Description": "Learn the Leave No Trace Principles for Kids and your responsibility to protect the outdoors for future generations.", "Required": True},
    {"Req_ID": "TigersInTheWild.4", "Adventure": "Tigers in the Wild", "Requirement_Description": "Identify three animals and insects that might harm you or make you sick on the outside adventure. Explain how you can help protect yourself from each.", "Required": True},
    {"Req_ID": "TigersInTheWild.5", "Adventure": "Tigers in the Wild", "Requirement_Description": "Go on a 1-mile walk outside with your den or family.", "Required": True},

    # Elective Adventures (Complete any 2)
    # Champions for Nature Tiger (4 requirements)
    {"Req_ID": "ChampionsNatureTiger.1", "Adventure": "Champions for Nature Tiger", "Requirement_Description": "Play a game where you are an animal that needs to find food, water, shelter, and space.", "Required": False},
    {"Req_ID": "ChampionsNatureTiger.2", "Adventure": "Champions for Nature Tiger", "Requirement_Description": "Discover an animal that is threatened or endangered. Learn how you can help.", "Required": False},
    {"Req_ID": "ChampionsNatureTiger.3", "Adventure": "Champions for Nature Tiger", "Requirement_Description": "Visit a zoo, a wild animal park, or another natural place. Tell what you saw while you were there.", "Required": False},
    {"Req_ID": "ChampionsNatureTiger.4", "Adventure": "Champions for Nature Tiger", "Requirement_Description": "Participate in a conservation service project.", "Required": False},

    # Curiosity, Intrigue, and Magical Mysteries (5 requirements)
    {"Req_ID": "CuriosityIntrigue.1", "Adventure": "Curiosity, Intrigue, and Magical Mysteries", "Requirement_Description": "Learn a magic trick. Show your den or family.", "Required": False},
    {"Req_ID": "CuriosityIntrigue.2", "Adventure": "Curiosity, Intrigue, and Magical Mysteries", "Requirement_Description": "Create a poster or picture showing what you like about magic.", "Required": False},
    {"Req_ID": "CuriosityIntrigue.3", "Adventure": "Curiosity, Intrigue, and Magical Mysteries", "Requirement_Description": "Learn a new skill. Show it to your den or family.", "Required": False},
    {"Req_ID": "CuriosityIntrigue.4", "Adventure": "Curiosity, Intrigue, and Magical Mysteries", "Requirement_Description": "Make an art sculpture or craft project.", "Required": False},
    {"Req_ID": "CuriosityIntrigue.5", "Adventure": "Curiosity, Intrigue, and Magical Mysteries", "Requirement_Description": "Watch a magic show.", "Required": False},

    # Designed by Tiger (4 requirements)
    {"Req_ID": "DesignedByTiger.1", "Adventure": "Designed by Tiger", "Requirement_Description": "Discover what an architect does.", "Required": False},
    {"Req_ID": "DesignedByTiger.2", "Adventure": "Designed by Tiger", "Requirement_Description": "Look at a house or building from the outside and identify three different geometric shapes you see.", "Required": False},
    {"Req_ID": "DesignedByTiger.3", "Adventure": "Designed by Tiger", "Requirement_Description": "Build a free-standing, tower structure at least 12 inches tall.", "Required": False},
    {"Req_ID": "DesignedByTiger.4", "Adventure": "Designed by Tiger", "Requirement_Description": "Make a cardboard model of a room in a home.", "Required": False},

    # Fish On (4 requirements)
    {"Req_ID": "FishOn.1", "Adventure": "Fish On", "Requirement_Description": "Discover how to get a fishing license, what kinds of fish can be caught, and what the laws are where you want to go fishing.", "Required": False},
    {"Req_ID": "FishOn.2", "Adventure": "Fish On", "Requirement_Description": "Discover the different types of fishing gear.", "Required": False},
    {"Req_ID": "FishOn.3", "Adventure": "Fish On", "Requirement_Description": "Make a simple fishing pole.", "Required": False},
    {"Req_ID": "FishOn.4", "Adventure": "Fish On", "Requirement_Description": "Go on a fishing adventure with your den or with your family, and catch a fish.", "Required": False},

    # Floats and Boats (5 requirements)
    {"Req_ID": "FloatsBoats.1", "Adventure": "Floats and Boats", "Requirement_Description": "Discover what makes something sink or float.", "Required": False},
    {"Req_ID": "FloatsBoats.2", "Adventure": "Floats and Boats", "Requirement_Description": "Make a boat out of recycled materials.", "Required": False},
    {"Req_ID": "FloatsBoats.3", "Adventure": "Floats and Boats", "Requirement_Description": "Make a boat move without touching it.", "Required": False},
    {"Req_ID": "FloatsBoats.4", "Adventure": "Floats and Boats", "Requirement_Description": "Learn the rules for boating safety and what to do in case of an emergency.", "Required": False},
    {"Req_ID": "FloatsBoats.5", "Adventure": "Floats and Boats", "Requirement_Description": "Discover what a life jacket is and how to wear it safely.", "Required": False},

    # Good Knights (4 requirements)
    {"Req_ID": "GoodKnights.1", "Adventure": "Good Knights", "Requirement_Description": "Learn about chivalry and knights. Learn how chivalry relates to how we behave today.", "Required": False},
    {"Req_ID": "GoodKnights.2", "Adventure": "Good Knights", "Requirement_Description": "Create your own code of conduct.", "Required": False},
    {"Req_ID": "GoodKnights.3", "Adventure": "Good Knights", "Requirement_Description": "Make a medieval sword and shield.", "Required": False},
    {"Req_ID": "GoodKnights.4", "Adventure": "Good Knights", "Requirement_Description": "Participate in a game or games that use a medieval theme.", "Required": False},

    # Let's Camp Tiger (4 requirements)
    {"Req_ID": "LetsCampTiger.1", "Adventure": "Let's Camp Tiger", "Requirement_Description": "Discover what to bring to a campout.", "Required": False},
    {"Req_ID": "LetsCampTiger.2", "Adventure": "Let's Camp Tiger", "Requirement_Description": "Discover what you need to sleep comfortably outdoors.", "Required": False},
    {"Req_ID": "LetsCampTiger.3", "Adventure": "Let's Camp Tiger", "Requirement_Description": "Learn how to set up a tent. Help put one up.", "Required": False},
    {"Req_ID": "LetsCampTiger.4", "Adventure": "Let's Camp Tiger", "Requirement_Description": "Participate in an outdoor campout with your den or family.", "Required": False},

    # Race Time Tiger (5 requirements)
    {"Req_ID": "RaceTimeTiger.1", "Adventure": "Race Time Tiger", "Requirement_Description": "With an adult, build either a Pinewood Derby car or a Raingutter Regatta boat.", "Required": False},
    {"Req_ID": "RaceTimeTiger.2", "Adventure": "Race Time Tiger", "Requirement_Description": "Learn the rules of the race for the vehicle chosen in requirement 1.", "Required": False},
    {"Req_ID": "RaceTimeTiger.3", "Adventure": "Race Time Tiger", "Requirement_Description": "Before the race, discuss with your den how you will demonstrate good sportsmanship.", "Required": False},
    {"Req_ID": "RaceTimeTiger.4", "Adventure": "Race Time Tiger", "Requirement_Description": "Participate in a Pinewood Derby or a Raingutter Regatta.", "Required": False},
    {"Req_ID": "RaceTimeTiger.5", "Adventure": "Race Time Tiger", "Requirement_Description": "Cheer for others who participate.", "Required": False},

    # Rolling Tigers (4 requirements)
    {"Req_ID": "RollingTigers.1", "Adventure": "Rolling Tigers", "Requirement_Description": "With your den or family, pick one type of wheeled vehicle and explore how it moves by doing one of the following: rolling, pedaling, or being pulled.", "Required": False},
    {"Req_ID": "RollingTigers.2", "Adventure": "Rolling Tigers", "Requirement_Description": "Discover how to stay safe when you are riding a bike or scooter.", "Required": False},
    {"Req_ID": "RollingTigers.3", "Adventure": "Rolling Tigers", "Requirement_Description": "Go on a bike or scooter ride with your family or den.", "Required": False},
    {"Req_ID": "RollingTigers.4", "Adventure": "Rolling Tigers", "Requirement_Description": "Make a wheeled vehicle.", "Required": False},

    # Safe and Smart (5 requirements)
    {"Req_ID": "SafeAndSmart.1", "Adventure": "Safe and Smart", "Requirement_Description": "Do the following: 1a. With your parent or legal guardian, complete the exercises in 'How to Protect Your Children from Child Abuse: A Parent's Guide.' 1b. Learn about tricky people.", "Required": False},
    {"Req_ID": "SafeAndSmart.2", "Adventure": "Safe and Smart", "Requirement_Description": "Learn what to do if you become lost.", "Required": False},
    {"Req_ID": "SafeAndSmart.3", "Adventure": "Safe and Smart", "Requirement_Description": "Learn about fire and burn safety. Make a fire escape plan with your family.", "Required": False},
    {"Req_ID": "SafeAndSmart.4", "Adventure": "Safe and Smart", "Requirement_Description": "Learn about stranger danger.", "Required": False},
    {"Req_ID": "SafeAndSmart.5", "Adventure": "Safe and Smart", "Requirement_Description": "Learn what to do if there is an emergency at home.", "Required": False},

    # Sky is the Limit (5 requirements)
    {"Req_ID": "SkyIsTheLimit.1", "Adventure": "Sky is the Limit", "Requirement_Description": "Explore what people can see in the sky.", "Required": False},
    {"Req_ID": "SkyIsTheLimit.2", "Adventure": "Sky is the Limit", "Requirement_Description": "Observe the sky during the day and night.", "Required": False},
    {"Req_ID": "SkyIsTheLimit.3", "Adventure": "Sky is the Limit", "Requirement_Description": "Make and use a pinhole projector or use a telescope to observe the moon.", "Required": False},
    {"Req_ID": "SkyIsTheLimit.4", "Adventure": "Sky is the Limit", "Requirement_Description": "Discover what controls the weather.", "Required": False},
    {"Req_ID": "SkyIsTheLimit.5", "Adventure": "Sky is the Limit", "Requirement_Description": "Learn about clouds and what they mean to weather. Watch the clouds and record what you see.", "Required": False},

    # Stories in Shapes (4 requirements)
    {"Req_ID": "StoriesInShapes.1", "Adventure": "Stories in Shapes", "Requirement_Description": "Explore what shapes are and how they are used.", "Required": False},
    {"Req_ID": "StoriesInShapes.2", "Adventure": "Stories in Shapes", "Requirement_Description": "Make a picture using shapes.", "Required": False},
    {"Req_ID": "StoriesInShapes.3", "Adventure": "Stories in Shapes", "Requirement_Description": "Find shapes in nature.", "Required": False},
    {"Req_ID": "StoriesInShapes.4", "Adventure": "Stories in Shapes", "Requirement_Description": "Create a piece of art by combining different shapes.", "Required": False},

    # Summertime Fun Tiger (1 requirement)
    {"Req_ID": "SummertimeFunTiger.1", "Adventure": "Summertime Fun Tiger", "Requirement_Description": "Anytime during May through August participate in a total of three Cub Scout activities.", "Required": False},

    # Tech All Around (4 requirements)
    {"Req_ID": "TechAllAround.1", "Adventure": "Tech All Around", "Requirement_Description": "Discover what technology is and how people use it in their lives.", "Required": False},
    {"Req_ID": "TechAllAround.2", "Adventure": "Tech All Around", "Requirement_Description": "Learn about the SAFE technology rules.", "Required": False},
    {"Req_ID": "TechAllAround.3", "Adventure": "Tech All Around", "Requirement_Description": "Make a list of devices you and your family use.", "Required": False},
    {"Req_ID": "TechAllAround.4", "Adventure": "Tech All Around", "Requirement_Description": "Learn how to find people who can help you with technology questions.", "Required": False},

    # Tiger Tag (5 requirements)
    {"Req_ID": "TigerTag.1", "Adventure": "Tiger Tag", "Requirement_Description": "With your den or with your family, play a game of tag.", "Required": False},
    {"Req_ID": "TigerTag.2", "Adventure": "Tiger Tag", "Requirement_Description": "Learn about being a good sport.", "Required": False},
    {"Req_ID": "TigerTag.3", "Adventure": "Tiger Tag", "Requirement_Description": "Make up a new version of tag and play it with your den.", "Required": False},
    {"Req_ID": "TigerTag.4", "Adventure": "Tiger Tag", "Requirement_Description": "Learn about eye safety.", "Required": False},
    {"Req_ID": "TigerTag.5", "Adventure": "Tiger Tag", "Requirement_Description": "During a den meeting or den outing, demonstrate how to use one of the following: A) an athletic cup, B) a mouthguard, C) safety glasses, or D) a protective helmet.", "Required": False},

    # Tiger-iffic! (5 requirements)
    {"Req_ID": "Tigeriffic.1", "Adventure": "Tiger-iffic!", "Requirement_Description": "Play a board game or another inside game with one or more members of your den.", "Required": False},
    {"Req_ID": "Tigeriffic.2", "Adventure": "Tiger-iffic!", "Requirement_Description": "With your adult partner or other family members, discover how to stay safe when using the internet.", "Required": False},
    {"Req_ID": "Tigeriffic.3", "Adventure": "Tiger-iffic!", "Requirement_Description": "Build a cardboard or pillow fort with the members of your den or family.", "Required": False},
    {"Req_ID": "Tigeriffic.4", "Adventure": "Tiger-iffic!", "Requirement_Description": "Make a family scrapbook.", "Required": False},
    {"Req_ID": "Tigeriffic.5", "Adventure": "Tiger-iffic!", "Requirement_Description": "Visit a library or bookstore with your adult partner or den. Discover the different types of books you can check out or read.", "Required": False},

    # Tigers in the Water (4 requirements)
    {"Req_ID": "TigersInTheWater.1", "Adventure": "Tigers in the Water", "Requirement_Description": "State the safety precautions you need to take before doing any water activity.", "Required": False},
    {"Req_ID": "TigersInTheWater.2", "Adventure": "Tigers in the Water", "Requirement_Description": "Explain the meaning of 'order of rescue' and demonstrate reaching and throwing rescue techniques from land.", "Required": False},
    {"Req_ID": "TigersInTheWater.3", "Adventure": "Tigers in the Water", "Requirement_Description": "Attempt to glide at least 3 feet across the water.", "Required": False},
    {"Req_ID": "TigersInTheWater.4", "Adventure": "Tigers in the Water", "Requirement_Description": "Have 30 minutes, or more, of free swim time where you practice the buddy system and stay within your ability group.", "Required": False},
]

# Wolf Scout Requirements (2nd Grade)
WOLF_REQUIREMENTS = [
    # Required Adventures (6 total)
    # Bobcat Wolf (7 requirements)
    {"Req_ID": "BobcatWolf.1", "Adventure": "Bobcat Wolf", "Requirement_Description": "Get to know members of your den.", "Required": True},
    {"Req_ID": "BobcatWolf.2", "Adventure": "Bobcat Wolf", "Requirement_Description": "Recite the Scout Oath and Law with your den and den leader.", "Required": True},
    {"Req_ID": "BobcatWolf.3", "Adventure": "Bobcat Wolf", "Requirement_Description": "Learn about the Scout Oath and Scout Law. Discover what the Scout Law means.", "Required": True},
    {"Req_ID": "BobcatWolf.4", "Adventure": "Bobcat Wolf", "Requirement_Description": "With your den create a den Code of Conduct.", "Required": True},
    {"Req_ID": "BobcatWolf.5", "Adventure": "Bobcat Wolf", "Requirement_Description": "Learn about the denner position and responsibilities.", "Required": True},
    {"Req_ID": "BobcatWolf.6", "Adventure": "Bobcat Wolf", "Requirement_Description": "Demonstrate the Cub Scout sign, Cub Scout salute, and Cub Scout handshake. Show how each is used.", "Required": True},
    {"Req_ID": "BobcatWolf.7", "Adventure": "Bobcat Wolf", "Requirement_Description": "At home, with your parent or legal guardian do the activities in the booklet 'How to Protect Your Children from Child Abuse: A Parent's Guide.'", "Required": True},

    # Running With the Pack (6 requirements)
    {"Req_ID": "RunningWithThePack.1", "Adventure": "Running With the Pack", "Requirement_Description": "Sample foods from each of the following food groups: protein, vegetables, fruits, dairy, and grains.", "Required": True},
    {"Req_ID": "RunningWithThePack.2", "Adventure": "Running With the Pack", "Requirement_Description": "Be active for 30 minutes with your den or at least one other person that includes both stretching and moving.", "Required": True},
    {"Req_ID": "RunningWithThePack.3", "Adventure": "Running With the Pack", "Requirement_Description": "Be active for 15 minutes doing personal exercises that include cardio, muscular strength, and flexibility.", "Required": True},
    {"Req_ID": "RunningWithThePack.4", "Adventure": "Running With the Pack", "Requirement_Description": "Do a relaxing activity for 10 minutes.", "Required": True},
    {"Req_ID": "RunningWithThePack.5", "Adventure": "Running With the Pack", "Requirement_Description": "Review your Scouting America Annual Health and Medical record with your parent or guardian. Discuss your ability to participate in den and pack activities.", "Required": True},
    {"Req_ID": "RunningWithThePack.6", "Adventure": "Running With the Pack", "Requirement_Description": "Learn what it means to be physically fit.", "Required": True},

    # Safety in Numbers (4 requirements)
    {"Req_ID": "SafetyInNumbers.1", "Adventure": "Safety in Numbers", "Requirement_Description": "With permission from your parent or legal guardian, watch the Protect Yourself Rules video for the Wolf rank.", "Required": True},
    {"Req_ID": "SafetyInNumbers.2", "Adventure": "Safety in Numbers", "Requirement_Description": "Complete the Personal Space Bubble worksheet that is part of the Protect Yourself Rules resources.", "Required": True},
    {"Req_ID": "SafetyInNumbers.3", "Adventure": "Safety in Numbers", "Requirement_Description": "With your parent or legal guardian, set up a family policy for digital devices.", "Required": True},
    {"Req_ID": "SafetyInNumbers.4", "Adventure": "Safety in Numbers", "Requirement_Description": "Learn the buddy system for different types of activities, including outdoor activities, school activities, online interactions, and everyday interactions with others.", "Required": True},

    # Footsteps (4 requirements)
    {"Req_ID": "Footsteps.1", "Adventure": "Footsteps", "Requirement_Description": "With your parent or legal guardian, talk about your family's faith traditions. Identify three holidays or celebrations that are part of your family's faith traditions. Make a craft, work of art, or a food item that is part of your favorite family's faith tradition, holiday, or celebration.", "Required": True},
    {"Req_ID": "Footsteps.2", "Adventure": "Footsteps", "Requirement_Description": "With your family, attend a religious service OR other gathering that shows how your family expresses reverence.", "Required": True},
    {"Req_ID": "Footsteps.3", "Adventure": "Footsteps", "Requirement_Description": "Carry out an act of kindness.", "Required": True},
    {"Req_ID": "Footsteps.4", "Adventure": "Footsteps", "Requirement_Description": "With your parent or legal guardian identify a religion or faith that is different from your own. Determine two things that it has in common with your family's beliefs.", "Required": True},

    # Council Fire (6 requirements)
    {"Req_ID": "CouncilFire.1", "Adventure": "Council Fire", "Requirement_Description": "Discover what being a good citizen means.", "Required": True},
    {"Req_ID": "CouncilFire.2", "Adventure": "Council Fire", "Requirement_Description": "Demonstrate good citizenship by showing respect for the flag of the United States of America. Show how to properly display it and how to fold it.", "Required": True},
    {"Req_ID": "CouncilFire.3", "Adventure": "Council Fire", "Requirement_Description": "Participate in a flag ceremony.", "Required": True},
    {"Req_ID": "CouncilFire.4", "Adventure": "Council Fire", "Requirement_Description": "Learn about the mission of any non-profit. Find out how they fund their activities and how volunteers are used to help.", "Required": True},
    {"Req_ID": "CouncilFire.5", "Adventure": "Council Fire", "Requirement_Description": "Participate in a service project.", "Required": True},
    {"Req_ID": "CouncilFire.6", "Adventure": "Council Fire", "Requirement_Description": "Discover a state symbol. Make a model, work of art, or other craft that depicts the symbol you chose.", "Required": True},

    # Paws on the Path (5 requirements)
    {"Req_ID": "PawsOnThePath.1", "Adventure": "Paws on the Path", "Requirement_Description": "Prepare for a one-mile walk by gathering the Cub Scout Six Essentials and weather appropriate clothing and shoes.", "Required": True},
    {"Req_ID": "PawsOnThePath.2", "Adventure": "Paws on the Path", "Requirement_Description": "Learn what SAW (Stay, Answer, Whistle) means. Discover when you might need to use it.", "Required": True},
    {"Req_ID": "PawsOnThePath.3", "Adventure": "Paws on the Path", "Requirement_Description": "Discover the Leave No Trace Principles for Kids and your responsibility to protect the outdoors for future generations.", "Required": True},
    {"Req_ID": "PawsOnThePath.4", "Adventure": "Paws on the Path", "Requirement_Description": "Go on your one-mile walk while practicing the Leave No Trace Principles for Kids.", "Required": True},
    {"Req_ID": "PawsOnThePath.5", "Adventure": "Paws on the Path", "Requirement_Description": "After your walk, make a list of three things you saw on your walk and share it with your family.", "Required": True},

    # Elective Adventures (Complete any 2)
    # A Wolf Goes Fishing (4 requirements)
    {"Req_ID": "AWolfGoesFishing.1", "Adventure": "A Wolf Goes Fishing", "Requirement_Description": "Make a plan to go fishing. Determine where you will go and what type of fish you plan to catch. All of the following requirements are to be completed based on your choice.", "Required": False},
    {"Req_ID": "AWolfGoesFishing.2", "Adventure": "A Wolf Goes Fishing", "Requirement_Description": "Use the Scouting America S.A.F.E. Checklist to plan what you need for your fishing experience.", "Required": False},
    {"Req_ID": "AWolfGoesFishing.3", "Adventure": "A Wolf Goes Fishing", "Requirement_Description": "Choose a design, gather materials, and make a fishing lure or fly.", "Required": False},
    {"Req_ID": "AWolfGoesFishing.4", "Adventure": "A Wolf Goes Fishing", "Requirement_Description": "Following local and state guidelines, go on a fishing adventure with your den or family. Follow all fishing regulations and proper fish handling techniques.", "Required": False},

    # Adventures in Coins (5 requirements)
    {"Req_ID": "AdventuresInCoins.1", "Adventure": "Adventures in Coins", "Requirement_Description": "Identify different parts of a coin.", "Required": False},
    {"Req_ID": "AdventuresInCoins.2", "Adventure": "Adventures in Coins", "Requirement_Description": "Find the mint mark on a coin; identify what mint facility it came from and what year it was made.", "Required": False},
    {"Req_ID": "AdventuresInCoins.3", "Adventure": "Adventures in Coins", "Requirement_Description": "Choose a coin that interests you, and make a coin rubbing. List information next to the coin detailing the pictures on it, the year it was made, and the mint where it was made.", "Required": False},
    {"Req_ID": "AdventuresInCoins.4", "Adventure": "Adventures in Coins", "Requirement_Description": "Play a coin game.", "Required": False},
    {"Req_ID": "AdventuresInCoins.5", "Adventure": "Adventures in Coins", "Requirement_Description": "Create a balance scale and show how it balances.", "Required": False},

    # Air of the Wolf (4 requirements)
    {"Req_ID": "AirOfTheWolf.1", "Adventure": "Air of the Wolf", "Requirement_Description": "Conduct an investigation on how well different materials insulate against heat loss.", "Required": False},
    {"Req_ID": "AirOfTheWolf.2", "Adventure": "Air of the Wolf", "Requirement_Description": "Conduct an investigation on what happens when air is warmed.", "Required": False},
    {"Req_ID": "AirOfTheWolf.3", "Adventure": "Air of the Wolf", "Requirement_Description": "Make and record observations of weather conditions over a one-week period.", "Required": False},
    {"Req_ID": "AirOfTheWolf.4", "Adventure": "Air of the Wolf", "Requirement_Description": "Participate in a total of three Cub Scout activities at home, at school, or in your community during the months of June, July, and August.", "Required": False},

    # Champions for Nature Wolf (5 requirements)
    {"Req_ID": "ChampionsNatureWolf.1", "Adventure": "Champions for Nature Wolf", "Requirement_Description": "Discover the four components that make up a habitat: food, water, shelter, space.", "Required": False},
    {"Req_ID": "ChampionsNatureWolf.2", "Adventure": "Champions for Nature Wolf", "Requirement_Description": "Pick an animal that is currently threatened or endangered to complete requirements 3, 4, and 5.", "Required": False},
    {"Req_ID": "ChampionsNatureWolf.3", "Adventure": "Champions for Nature Wolf", "Requirement_Description": "Identify the characteristics that classify an animal as a threatened or endangered species.", "Required": False},
    {"Req_ID": "ChampionsNatureWolf.4", "Adventure": "Champions for Nature Wolf", "Requirement_Description": "Explore what caused this animal to be threatened or endangered.", "Required": False},
    {"Req_ID": "ChampionsNatureWolf.5", "Adventure": "Champions for Nature Wolf", "Requirement_Description": "Research what is currently being done to protect the animal and participate in a conservation service project.", "Required": False},

    # Code of the Wolf (4 requirements)
    {"Req_ID": "CodeOfTheWolf.1", "Adventure": "Code of the Wolf", "Requirement_Description": "Discover what it means to be a good digital citizen.", "Required": False},
    {"Req_ID": "CodeOfTheWolf.2", "Adventure": "Code of the Wolf", "Requirement_Description": "Demonstrate your knowledge of cyberbullying and what you can do when you see it.", "Required": False},
    {"Req_ID": "CodeOfTheWolf.3", "Adventure": "Code of the Wolf", "Requirement_Description": "With the help of your parent or legal guardian, send an email message to someone.", "Required": False},
    {"Req_ID": "CodeOfTheWolf.4", "Adventure": "Code of the Wolf", "Requirement_Description": "With your den or an adult, use the internet to find information on a topic of interest to you, or play a game or other activity.", "Required": False},

    # Computing Wolves (5 requirements)
    {"Req_ID": "ComputingWolves.1", "Adventure": "Computing Wolves", "Requirement_Description": "Do the following: 1a. Visit a company, organization, or institution where you can observe how technology is used and talk to someone who works there. 1b. Identify how technology is utilized to solve a problem or make something better.", "Required": False},
    {"Req_ID": "ComputingWolves.2", "Adventure": "Computing Wolves", "Requirement_Description": "Explore with your den or an adult how to stay safe when using the internet.", "Required": False},
    {"Req_ID": "ComputingWolves.3", "Adventure": "Computing Wolves", "Requirement_Description": "Do the following: 3a. With the help of your parent or legal guardian, watch a video or read a book about computer coding or a coder. 3b. Discuss what you learned about coding or coders.", "Required": False},
    {"Req_ID": "ComputingWolves.4", "Adventure": "Computing Wolves", "Requirement_Description": "Create an algorithm for a device in your everyday life.", "Required": False},
    {"Req_ID": "ComputingWolves.5", "Adventure": "Computing Wolves", "Requirement_Description": "Find out where the CPU and motherboard are located in your computer.", "Required": False},

    # Cubs Who Care (4 requirements)
    {"Req_ID": "CubsWhoCare.1", "Adventure": "Cubs Who Care", "Requirement_Description": "Visit a nature center, zoo, or another facility that cares for animals. During your visit, talk to someone who works with the animals.", "Required": False},
    {"Req_ID": "CubsWhoCare.2", "Adventure": "Cubs Who Care", "Requirement_Description": "Learn what it takes to care for a pet in your home. Make a poster about the care needed by your pet or a pet that you would like to have.", "Required": False},
    {"Req_ID": "CubsWhoCare.3", "Adventure": "Cubs Who Care", "Requirement_Description": "Learn about the care that aquarium fish need. OR Learn about the care that fish in the wild need in order to stay healthy.", "Required": False},
    {"Req_ID": "CubsWhoCare.4", "Adventure": "Cubs Who Care", "Requirement_Description": "Discover what 'cruelty to animals' means.", "Required": False},

    # Digging in the Past (4 requirements)
    {"Req_ID": "DiggingInThePast.1", "Adventure": "Digging in the Past", "Requirement_Description": "Discover what archeology is and what an archeologist does. Learn about a archeologist or paleontologist and what he or she is working on.", "Required": False},
    {"Req_ID": "DiggingInThePast.2", "Adventure": "Digging in the Past", "Requirement_Description": "Learn about the history of your community, a building in your community, or a street in your community. Draw or create a model of your artifact.", "Required": False},
    {"Req_ID": "DiggingInThePast.3", "Adventure": "Digging in the Past", "Requirement_Description": "Create a record of the history of Scouting in your family.", "Required": False},
    {"Req_ID": "DiggingInThePast.4", "Adventure": "Digging in the Past", "Requirement_Description": "Examine how an archeologist records things and make a record of an artifact at home or a location where you live.", "Required": False},

    # Finding Your Way (4 requirements)
    {"Req_ID": "FindingYourWay.1", "Adventure": "Finding Your Way", "Requirement_Description": "Explore how to find directions using a compass. Discover how to determine cardinal directions without a compass.", "Required": False},
    {"Req_ID": "FindingYourWay.2", "Adventure": "Finding Your Way", "Requirement_Description": "Identify all of the cardinal directions on a map. Locate three different places you would like to visit on the map.", "Required": False},
    {"Req_ID": "FindingYourWay.3", "Adventure": "Finding Your Way", "Requirement_Description": "Create a map of your neighborhood. Show natural and manmade features.", "Required": False},
    {"Req_ID": "FindingYourWay.4", "Adventure": "Finding Your Way", "Requirement_Description": "Use a map and compass or a GPS to go on a hike or outdoor adventure with your family or den.", "Required": False},

    # Germs Alive! (4 requirements)
    {"Req_ID": "GermsAlive.1", "Adventure": "Germs Alive!", "Requirement_Description": "Discover what germs are and how they affect your body.", "Required": False},
    {"Req_ID": "GermsAlive.2", "Adventure": "Germs Alive!", "Requirement_Description": "Demonstrate proper hand-washing techniques. Explain why hand washing is important.", "Required": False},
    {"Req_ID": "GermsAlive.3", "Adventure": "Germs Alive!", "Requirement_Description": "Conduct an investigation to discover what happens when you don't wash your hands. Share what you learned.", "Required": False},
    {"Req_ID": "GermsAlive.4", "Adventure": "Germs Alive!", "Requirement_Description": "Learn about how immunizations work to prevent disease.", "Required": False},

    # Let's Camp Wolf (5 requirements)
    {"Req_ID": "LetsCampWolf.1", "Adventure": "Let's Camp Wolf", "Requirement_Description": "With your den, pack, or family, plan and participate in a campout.", "Required": False},
    {"Req_ID": "LetsCampWolf.2", "Adventure": "Let's Camp Wolf", "Requirement_Description": "Upon arrival at the campground, determine where to set up your tent.", "Required": False},
    {"Req_ID": "LetsCampWolf.3", "Adventure": "Let's Camp Wolf", "Requirement_Description": "Set up your tent with the help of an adult. Determine a safe place to put your camping equipment inside the tent.", "Required": False},
    {"Req_ID": "LetsCampWolf.4", "Adventure": "Let's Camp Wolf", "Requirement_Description": "Upon arrival at the campground, discuss with an adult what makes a good campfire location and determine a safe place to build a campfire.", "Required": False},
    {"Req_ID": "LetsCampWolf.5", "Adventure": "Let's Camp Wolf", "Requirement_Description": "After your campout, share the things you did to follow the Outdoor Code and Leave No Trace Principles for Kids with your den or family.", "Required": False},

    # Paws for Water (4 requirements)
    {"Req_ID": "PawsForWater.1", "Adventure": "Paws for Water", "Requirement_Description": "State the safety precautions you need to take before doing any water activity.", "Required": False},
    {"Req_ID": "PawsForWater.2", "Adventure": "Paws for Water", "Requirement_Description": "Explain the meaning of 'order of rescue' and demonstrate reaching and throwing rescue techniques from land.", "Required": False},
    {"Req_ID": "PawsForWater.3", "Adventure": "Paws for Water", "Requirement_Description": "Attempt to float on your back with minimum movement for at least 15 seconds.", "Required": False},
    {"Req_ID": "PawsForWater.4", "Adventure": "Paws for Water", "Requirement_Description": "Have 30 minutes, or more, of free swim time where you practice the buddy system and stay within your ability group. The qualified adult supervision should conduct at least three buddy checks per half hour swimming.", "Required": False},

    # Paws of Skill (4 requirements)
    {"Req_ID": "PawsOfSkill.1", "Adventure": "Paws of Skill", "Requirement_Description": "Learn about the history of the American circus and discover the different acts. OR Learn about the history of another circus, such as the Chinese or Mexican circus, and discover the different acts.", "Required": False},
    {"Req_ID": "PawsOfSkill.2", "Adventure": "Paws of Skill", "Requirement_Description": "Balance yourself on one foot for 30 seconds; then do this on the other foot.", "Required": False},
    {"Req_ID": "PawsOfSkill.3", "Adventure": "Paws of Skill", "Requirement_Description": "Practice juggling with at least two juggling balls or bean bags.", "Required": False},
    {"Req_ID": "PawsOfSkill.4", "Adventure": "Paws of Skill", "Requirement_Description": "Walk 10 steps on a line or make a line and walk 10 steps backwards on the line.", "Required": False},

    # Pedal With the Pack (4 requirements)
    {"Req_ID": "PedalWithThePack.1", "Adventure": "Pedal With the Pack", "Requirement_Description": "Discover what gear and supplies you should bring for a long bike ride.", "Required": False},
    {"Req_ID": "PedalWithThePack.2", "Adventure": "Pedal With the Pack", "Requirement_Description": "Explain safety rules for using your bike.", "Required": False},
    {"Req_ID": "PedalWithThePack.3", "Adventure": "Pedal With the Pack", "Requirement_Description": "Show how to wear the proper safety equipment for bike riding.", "Required": False},
    {"Req_ID": "PedalWithThePack.4", "Adventure": "Pedal With the Pack", "Requirement_Description": "With your den, pack, or family and using the buddy system, go on a bike ride that is at least 2 miles.", "Required": False},

    # Race Time Wolf (5 requirements)
    {"Req_ID": "RaceTimeWolf.1", "Adventure": "Race Time Wolf", "Requirement_Description": "With an adult, build either a Pinewood Derby car or a Raingutter Regatta boat.", "Required": False},
    {"Req_ID": "RaceTimeWolf.2", "Adventure": "Race Time Wolf", "Requirement_Description": "Learn the rules of the race for the vehicle chosen in requirement 1.", "Required": False},
    {"Req_ID": "RaceTimeWolf.3", "Adventure": "Race Time Wolf", "Requirement_Description": "Before the race, discuss with your den how you will demonstrate good sportsmanship during the race.", "Required": False},
    {"Req_ID": "RaceTimeWolf.4", "Adventure": "Race Time Wolf", "Requirement_Description": "Participate in a Pinewood Derby or a Raingutter Regatta.", "Required": False},
    {"Req_ID": "RaceTimeWolf.5", "Adventure": "Race Time Wolf", "Requirement_Description": "Cheer for others who participate.", "Required": False},

    # Spirit of the Water (4 requirements)
    {"Req_ID": "SpiritOfTheWater.1", "Adventure": "Spirit of the Water", "Requirement_Description": "State the safety precautions you need to take before participating in boating.", "Required": False},
    {"Req_ID": "SpiritOfTheWater.2", "Adventure": "Spirit of the Water", "Requirement_Description": "Discover what it means to be a responsible boater and how you can demonstrate being a responsible boater on the water.", "Required": False},
    {"Req_ID": "SpiritOfTheWater.3", "Adventure": "Spirit of the Water", "Requirement_Description": "Explain the buddy system when boating.", "Required": False},
    {"Req_ID": "SpiritOfTheWater.4", "Adventure": "Spirit of the Water", "Requirement_Description": "While wearing a life jacket, explore the different swimming strokes used in various boats. Pretend that you are canoeing, kayaking, stand-up paddleboarding, or rowing.", "Required": False},

    # Summertime Fun Wolf (1 requirement)
    {"Req_ID": "SummertimeFunWolf.1", "Adventure": "Summertime Fun Wolf", "Requirement_Description": "Anytime during May through August participate in a total of three Cub Scout activities.", "Required": False},
]

# Bear Scout Requirements (3rd Grade)
BEAR_REQUIREMENTS = [
    # Required Adventures (6 total)
    # Bobcat Bear (8 requirements)
    {"Req_ID": "BobcatBear.1", "Adventure": "Bobcat Bear", "Requirement_Description": "Get to know members of your den.", "Required": True},
    {"Req_ID": "BobcatBear.2", "Adventure": "Bobcat Bear", "Requirement_Description": "Recite the Scout Oath and Law with your den and den leader.", "Required": True},
    {"Req_ID": "BobcatBear.3", "Adventure": "Bobcat Bear", "Requirement_Description": "Learn about the Scout Oath. Identify the three points of the Scout Oath.", "Required": True},
    {"Req_ID": "BobcatBear.4", "Adventure": "Bobcat Bear", "Requirement_Description": "With your den create a den Code of Conduct.", "Required": True},
    {"Req_ID": "BobcatBear.5", "Adventure": "Bobcat Bear", "Requirement_Description": "Learn about the denner position and responsibilities.", "Required": True},
    {"Req_ID": "BobcatBear.6", "Adventure": "Bobcat Bear", "Requirement_Description": "Demonstrate the Cub Scout sign, Cub Scout salute, and Cub Scout handshake. Show how each is used.", "Required": True},
    {"Req_ID": "BobcatBear.7", "Adventure": "Bobcat Bear", "Requirement_Description": "Share with your den, or family, a time when you demonstrated the Cub Scout motto 'Do Your Best.' Explain why it is important to do your best.", "Required": True},
    {"Req_ID": "BobcatBear.8", "Adventure": "Bobcat Bear", "Requirement_Description": "At home, with your parent or legal guardian do the activities in the booklet 'How to Protect Your Children from Child Abuse: A Parent's Guide.'", "Required": True},

    # Bear Strong (5 requirements)
    {"Req_ID": "BearStrong.1", "Adventure": "Bear Strong", "Requirement_Description": "Sample food from three of the following food groups: protein, vegetables, fruits, dairy, and grains.", "Required": True},
    {"Req_ID": "BearStrong.2", "Adventure": "Bear Strong", "Requirement_Description": "Be active for 30 minutes with your den or at least one other person that includes both stretching and moving.", "Required": True},
    {"Req_ID": "BearStrong.3", "Adventure": "Bear Strong", "Requirement_Description": "Be active for 15 minutes doing personal exercises that include cardio, muscular strength, and flexibility.", "Required": True},
    {"Req_ID": "BearStrong.4", "Adventure": "Bear Strong", "Requirement_Description": "Do a relaxing activity for 10 minutes.", "Required": True},
    {"Req_ID": "BearStrong.5", "Adventure": "Bear Strong", "Requirement_Description": "Review your Scouting America Annual Health and Medical record with your parent or guardian. Discuss your ability to participate in den and pack activities.", "Required": True},

    # Standing Tall (4 requirements)
    {"Req_ID": "StandingTall.1", "Adventure": "Standing Tall", "Requirement_Description": "With permission from your parent or legal guardian, watch the Protect Yourself Rules video for the Bear rank.", "Required": True},
    {"Req_ID": "StandingTall.2", "Adventure": "Standing Tall", "Requirement_Description": "Complete the Personal Space Bubble worksheet that is part of the Protect Yourself Rules resources.", "Required": True},
    {"Req_ID": "StandingTall.3", "Adventure": "Standing Tall", "Requirement_Description": "With your parent or legal guardian, set up a family policy for digital devices.", "Required": True},
    {"Req_ID": "StandingTall.4", "Adventure": "Standing Tall", "Requirement_Description": "Identify common personal safety gear for your head, eyes, mouth, hands, and feet. List how each of these items protect you. Demonstrate the proper use of personal safety gear for an activity.", "Required": True},

    # Fellowship (4 requirements)
    {"Req_ID": "Fellowship.1", "Adventure": "Fellowship", "Requirement_Description": "With your parent or legal guardian talk about your family's faith traditions. Identify three holidays or celebrations that are part of your family's faith traditions. Make a craft, work of art, or a food item that is part of your favorite family's faith tradition, holiday or celebration.", "Required": True},
    {"Req_ID": "Fellowship.2", "Adventure": "Fellowship", "Requirement_Description": "With your family, attend a religious service OR other gathering that shows how your family expresses reverence.", "Required": True},
    {"Req_ID": "Fellowship.3", "Adventure": "Fellowship", "Requirement_Description": "Carry out an act of kindness.", "Required": True},
    {"Req_ID": "Fellowship.4", "Adventure": "Fellowship", "Requirement_Description": "With your parent or legal guardian identify a religion or faith that is different from your own. Determine two things that it has in common with your family's beliefs.", "Required": True},

    # Paws for Action (4 requirements)
    {"Req_ID": "PawsForAction.1", "Adventure": "Paws for Action", "Requirement_Description": "Familiarize yourself with the flag of the United States of America including the history, demonstrating how to raise and lower the flag, how to properly fold and display, and the United States etiquette.", "Required": True},
    {"Req_ID": "PawsForAction.2", "Adventure": "Paws for Action", "Requirement_Description": "Identify 3 symbols that represent the United States. Pick your favorite and make a model, work of art, or other craft that depicts the symbol.", "Required": True},
    {"Req_ID": "PawsForAction.3", "Adventure": "Paws for Action", "Requirement_Description": "Learn about the mission of any non-profit. Find out how they fund their activities and how volunteers are used to help.", "Required": True},
    {"Req_ID": "PawsForAction.4", "Adventure": "Paws for Action", "Requirement_Description": "Participate in a service project.", "Required": True},

    # Bear Habitat (9 requirements)
    {"Req_ID": "BearHabitat.1", "Adventure": "Bear Habitat", "Requirement_Description": "Prepare for a one-mile walk by gathering the Cub Scout Six Essentials and weather appropriate clothing and shoes.", "Required": True},
    {"Req_ID": "BearHabitat.2", "Adventure": "Bear Habitat", "Requirement_Description": "'Know Before You Go' Identify the location of your walk on a map and confirm your one-mile route.", "Required": True},
    {"Req_ID": "BearHabitat.3", "Adventure": "Bear Habitat", "Requirement_Description": "'Choose the Right Path' Learn about the path and surrounding area you will be walking on.", "Required": True},
    {"Req_ID": "BearHabitat.4", "Adventure": "Bear Habitat", "Requirement_Description": "'Trash your Trash' Make a plan for what you will do with your personal trash or trash you find along the trail.", "Required": True},
    {"Req_ID": "BearHabitat.5", "Adventure": "Bear Habitat", "Requirement_Description": "'Leave What You Find' Take pictures along your walk or bring a sketchbook to draw five things that you want to remember on your walk.", "Required": True},
    {"Req_ID": "BearHabitat.6", "Adventure": "Bear Habitat", "Requirement_Description": "'Be Careful with Fire' Determine the fire danger rating along your path.", "Required": True},
    {"Req_ID": "BearHabitat.7", "Adventure": "Bear Habitat", "Requirement_Description": "'Respect Wildlife' From a safe distance, identify as you look up, down, and around you, six signs of any mammals, birds, insects, reptiles.", "Required": True},
    {"Req_ID": "BearHabitat.8", "Adventure": "Bear Habitat", "Requirement_Description": "'Be Kind to Other Visitors' Identify what you need to do as a den to be kind to others on the path.", "Required": True},
    {"Req_ID": "BearHabitat.9", "Adventure": "Bear Habitat", "Requirement_Description": "Go on your one-mile walk while practicing your Leave No Trace Principles for Kids.", "Required": True},

    # Elective Adventures (Complete any 2)
    # A Bear Goes Fishing (4 requirements)
    {"Req_ID": "ABearGoesFishing.1", "Adventure": "A Bear Goes Fishing", "Requirement_Description": "Make a plan to go fishing. Determine where you will go and what type of fish you plan to catch. All of the following requirements are to be completed based on your choice.", "Required": False},
    {"Req_ID": "ABearGoesFishing.2", "Adventure": "A Bear Goes Fishing", "Requirement_Description": "Use the Scouting America S.A.F.E. Checklist to plan what you need for your fishing experience.", "Required": False},
    {"Req_ID": "ABearGoesFishing.3", "Adventure": "A Bear Goes Fishing", "Requirement_Description": "Determine the best type of fishing gear to use. Have an adult review your fishing gear.", "Required": False},
    {"Req_ID": "ABearGoesFishing.4", "Adventure": "A Bear Goes Fishing", "Requirement_Description": "Following local and state guidelines, go on a fishing adventure with your den or family. Follow all fishing regulations and proper fish handling techniques.", "Required": False},

    # Balancing Bears (4 requirements)
    {"Req_ID": "BalancingBears.1", "Adventure": "Balancing Bears", "Requirement_Description": "Identify a personal interest or hobby that you could turn into a small business.", "Required": False},
    {"Req_ID": "BalancingBears.2", "Adventure": "Balancing Bears", "Requirement_Description": "Develop a business plan for your idea.", "Required": False},
    {"Req_ID": "BalancingBears.3", "Adventure": "Balancing Bears", "Requirement_Description": "Based on your business plan, create a marketing strategy.", "Required": False},
    {"Req_ID": "BalancingBears.4", "Adventure": "Balancing Bears", "Requirement_Description": "Implement your marketing strategy and sell your product or service.", "Required": False},

    # Baloo the Builder (5 requirements)
    {"Req_ID": "BalooTheBuilder.1", "Adventure": "Baloo the Builder", "Requirement_Description": "Discover the tools that are in a toolbox. Learn the safe way to use each tool.", "Required": False},
    {"Req_ID": "BalooTheBuilder.2", "Adventure": "Baloo the Builder", "Requirement_Description": "Learn how to measure using a tape measure.", "Required": False},
    {"Req_ID": "BalooTheBuilder.3", "Adventure": "Baloo the Builder", "Requirement_Description": "With the guidance of your Webelos den leader, parent, or legal guardian, select a carpentry project to build with your parent, den, or other adult partner.", "Required": False},
    {"Req_ID": "BalooTheBuilder.4", "Adventure": "Baloo the Builder", "Requirement_Description": "Build your carpentry project.", "Required": False},
    {"Req_ID": "BalooTheBuilder.5", "Adventure": "Baloo the Builder", "Requirement_Description": "Apply a finish to your carpentry project.", "Required": False},

    # Bears Afloat (5 requirements)
    {"Req_ID": "BearsAfloat.1", "Adventure": "Bears Afloat", "Requirement_Description": "Before attempting requirements 3, 4, and 5 for this Adventure, you must pass the Scouting America swimmer test.", "Required": False},
    {"Req_ID": "BearsAfloat.2", "Adventure": "Bears Afloat", "Requirement_Description": "Review Safety Afloat.", "Required": False},
    {"Req_ID": "BearsAfloat.3", "Adventure": "Bears Afloat", "Requirement_Description": "Demonstrate how to choose and properly wear a life jacket that is the correct size.", "Required": False},
    {"Req_ID": "BearsAfloat.4", "Adventure": "Bears Afloat", "Requirement_Description": "Explain how to stay safe on the water by staying away from the open water without a life jacket or without an adult.", "Required": False},
    {"Req_ID": "BearsAfloat.5", "Adventure": "Bears Afloat", "Requirement_Description": "Jump feet first into water over your head while wearing a life jacket. Then swim 25 feet wearing the life jacket.", "Required": False},

    # Bears on Bikes (5 requirements)
    {"Req_ID": "BearsOnBikes.1", "Adventure": "Bears on Bikes", "Requirement_Description": "Discover what gear and supplies you should bring for a long bike ride.", "Required": False},
    {"Req_ID": "BearsOnBikes.2", "Adventure": "Bears on Bikes", "Requirement_Description": "Practice fixing a flat tire.", "Required": False},
    {"Req_ID": "BearsOnBikes.3", "Adventure": "Bears on Bikes", "Requirement_Description": "Learn about bike safety and traffic safety rules.", "Required": False},
    {"Req_ID": "BearsOnBikes.4", "Adventure": "Bears on Bikes", "Requirement_Description": "Show how to wear the proper safety equipment for bike riding.", "Required": False},
    {"Req_ID": "BearsOnBikes.5", "Adventure": "Bears on Bikes", "Requirement_Description": "With your den, pack, or family and using the buddy system, go on a bicycle ride that is a minimum of 3 miles.", "Required": False},

    # Champions for Nature Bear (5 requirements)
    {"Req_ID": "ChampionsNatureBear.1", "Adventure": "Champions for Nature Bear", "Requirement_Description": "Discover the four components that make up a habitat: food, water, shelter, space.", "Required": False},
    {"Req_ID": "ChampionsNatureBear.2", "Adventure": "Champions for Nature Bear", "Requirement_Description": "Pick an animal that is currently threatened or endangered to complete requirements 3, 4, and 5.", "Required": False},
    {"Req_ID": "ChampionsNatureBear.3", "Adventure": "Champions for Nature Bear", "Requirement_Description": "Identify the characteristics that classify an animal as a threatened or endangered species.", "Required": False},
    {"Req_ID": "ChampionsNatureBear.4", "Adventure": "Champions for Nature Bear", "Requirement_Description": "Explore what caused this animal to be threatened or endangered.", "Required": False},
    {"Req_ID": "ChampionsNatureBear.5", "Adventure": "Champions for Nature Bear", "Requirement_Description": "Research what is currently being done to protect the animal and participate in a conservation service project.", "Required": False},

    # Chef Tech (5 requirements)
    {"Req_ID": "ChefTech.1", "Adventure": "Chef Tech", "Requirement_Description": "Identify six technological devices used to prepare food.", "Required": False},
    {"Req_ID": "ChefTech.2", "Adventure": "Chef Tech", "Requirement_Description": "Explain how three of the six devices identified in requirement 1 work.", "Required": False},
    {"Req_ID": "ChefTech.3", "Adventure": "Chef Tech", "Requirement_Description": "Using a device that is not powered by electricity or batteries, make a food item.", "Required": False},
    {"Req_ID": "ChefTech.4", "Adventure": "Chef Tech", "Requirement_Description": "With the help of an adult, prepare a food item using at least two different methods of food preparation: baking, boiling, simmering, roasting, frying, or grilling.", "Required": False},
    {"Req_ID": "ChefTech.5", "Adventure": "Chef Tech", "Requirement_Description": "Cook a food item from scratch using a recipe that requires ingredients you measure out.", "Required": False},

    # Critter Care (5 requirements)
    {"Req_ID": "CritterCare.1", "Adventure": "Critter Care", "Requirement_Description": "Discover three wild animals that live in your area. Explain how one of these animals survives in nature.", "Required": False},
    {"Req_ID": "CritterCare.2", "Adventure": "Critter Care", "Requirement_Description": "Learn what it takes to care for a dog or cat. Make a poster about the care needed for a dog, a cat, or another pet that you would like to have.", "Required": False},
    {"Req_ID": "CritterCare.3", "Adventure": "Critter Care", "Requirement_Description": "Visit a veterinarian and learn what a veterinarian does for your pet OR watch a video with a veterinarian to learn what the veterinarian does.", "Required": False},
    {"Req_ID": "CritterCare.4", "Adventure": "Critter Care", "Requirement_Description": "Discover an animal that is currently threatened or endangered.", "Required": False},
    {"Req_ID": "CritterCare.5", "Adventure": "Critter Care", "Requirement_Description": "Learn what 'cruelty to animals' means.", "Required": False},

    # Forensics (5 requirements)
    {"Req_ID": "Forensics.1", "Adventure": "Forensics", "Requirement_Description": "Discover what forensics is and how it is used to help solve crimes.", "Required": False},
    {"Req_ID": "Forensics.2", "Adventure": "Forensics", "Requirement_Description": "Analyze your fingerprints. Compare them to your family members' fingerprints.", "Required": False},
    {"Req_ID": "Forensics.3", "Adventure": "Forensics", "Requirement_Description": "Learn about chromatography and how it is used in forensics. Complete a chromatography investigation.", "Required": False},
    {"Req_ID": "Forensics.4", "Adventure": "Forensics", "Requirement_Description": "Discover how mystery powders are identified. Test four samples of mystery powders and identify what they are.", "Required": False},
    {"Req_ID": "Forensics.5", "Adventure": "Forensics", "Requirement_Description": "Explore the different techniques that are used to identify and collect evidence. Learn how the evidence is used to solve a crime. Participate in a crime scene investigation using evidence collection techniques.", "Required": False},

    # Let's Camp Bear (6 requirements)
    {"Req_ID": "LetsCampBear.1", "Adventure": "Let's Camp Bear", "Requirement_Description": "With your den, pack, or family, plan and participate in a campout.", "Required": False},
    {"Req_ID": "LetsCampBear.2", "Adventure": "Let's Camp Bear", "Requirement_Description": "Upon arrival at the campground, determine where to set up your tent.", "Required": False},
    {"Req_ID": "LetsCampBear.3", "Adventure": "Let's Camp Bear", "Requirement_Description": "Set up your tent without help from an adult.", "Required": False},
    {"Req_ID": "LetsCampBear.4", "Adventure": "Let's Camp Bear", "Requirement_Description": "Once your tents are set up, determine a safe place to build a campfire.", "Required": False},
    {"Req_ID": "LetsCampBear.5", "Adventure": "Let's Camp Bear", "Requirement_Description": "Show how to tie a bowline. Explain when this knot should be used and why. Explain what the word 'bight' means when using this knot.", "Required": False},
    {"Req_ID": "LetsCampBear.6", "Adventure": "Let's Camp Bear", "Requirement_Description": "After your campout, share the things you did to follow the Outdoor Code and Leave No Trace Principles for Kids with your den or family.", "Required": False},

    # Marble Madness (4 requirements)
    {"Req_ID": "MarbleMadness.1", "Adventure": "Marble Madness", "Requirement_Description": "Create a marble tray or marble maze.", "Required": False},
    {"Req_ID": "MarbleMadness.2", "Adventure": "Marble Madness", "Requirement_Description": "Learn about different types of marbles.", "Required": False},
    {"Req_ID": "MarbleMadness.3", "Adventure": "Marble Madness", "Requirement_Description": "Learn and demonstrate two different marble games.", "Required": False},
    {"Req_ID": "MarbleMadness.4", "Adventure": "Marble Madness", "Requirement_Description": "Complete a gravity investigation using marbles.", "Required": False},

    # Race Time Bear (5 requirements)
    {"Req_ID": "RaceTimeBear.1", "Adventure": "Race Time Bear", "Requirement_Description": "With an adult, build either a Pinewood Derby car or a Raingutter Regatta boat.", "Required": False},
    {"Req_ID": "RaceTimeBear.2", "Adventure": "Race Time Bear", "Requirement_Description": "Learn the rules of the race for the vehicle chosen in requirement 1.", "Required": False},
    {"Req_ID": "RaceTimeBear.3", "Adventure": "Race Time Bear", "Requirement_Description": "Explore the properties of friction and how it impacts your chosen vehicle.", "Required": False},
    {"Req_ID": "RaceTimeBear.4", "Adventure": "Race Time Bear", "Requirement_Description": "Before the race, discuss with your den how you will demonstrate good sportsmanship during the race.", "Required": False},
    {"Req_ID": "RaceTimeBear.5", "Adventure": "Race Time Bear", "Requirement_Description": "Participate in a Pinewood Derby or a Raingutter Regatta.", "Required": False},

    # Roaring Laughter (4 requirements)
    {"Req_ID": "RoaringLaughter.1", "Adventure": "Roaring Laughter", "Requirement_Description": "Develop a funny skit with your den or your family. OR Perform an original skit for your den, your pack, or your family.", "Required": False},
    {"Req_ID": "RoaringLaughter.2", "Adventure": "Roaring Laughter", "Requirement_Description": "Practice reading tongue-twisters. Perform one for your den, your pack, or your family.", "Required": False},
    {"Req_ID": "RoaringLaughter.3", "Adventure": "Roaring Laughter", "Requirement_Description": "Share at least one joke with your den at one of your den meetings.", "Required": False},
    {"Req_ID": "RoaringLaughter.4", "Adventure": "Roaring Laughter", "Requirement_Description": "Perform a magic trick for your den or your family.", "Required": False},

    # Salmon Run (4 requirements)
    {"Req_ID": "SalmonRun.1", "Adventure": "Salmon Run", "Requirement_Description": "Explain the importance of good sportsmanship.", "Required": False},
    {"Req_ID": "SalmonRun.2", "Adventure": "Salmon Run", "Requirement_Description": "Understand what it means to be physically fit. Discover how you can either maintain or improve your physical fitness.", "Required": False},
    {"Req_ID": "SalmonRun.3", "Adventure": "Salmon Run", "Requirement_Description": "Learn about the importance of stretching before and after any physical activity.", "Required": False},
    {"Req_ID": "SalmonRun.4", "Adventure": "Salmon Run", "Requirement_Description": "With your den, participate in the Cub Scout Sports program. Complete two of the four activities in a sport of your choosing.", "Required": False},

    # Summertime Fun Bear (1 requirement)
    {"Req_ID": "SummertimeFunBear.1", "Adventure": "Summertime Fun Bear", "Requirement_Description": "Anytime during May through August participate in a total of three Cub Scout activities.", "Required": False},

    # Super Science (4 requirements)
    {"Req_ID": "SuperScience.1", "Adventure": "Super Science", "Requirement_Description": "Do a science experiment.", "Required": False},
    {"Req_ID": "SuperScience.2", "Adventure": "Super Science", "Requirement_Description": "Visit a museum or visit with someone to discover more about science.", "Required": False},
    {"Req_ID": "SuperScience.3", "Adventure": "Super Science", "Requirement_Description": "Discuss with your family, your den, or other trusted adults how science affects your everyday life.", "Required": False},
    {"Req_ID": "SuperScience.4", "Adventure": "Super Science", "Requirement_Description": "Think like a computer programmer. Chart your day from wake-up to bedtime. Record the time that you spend on each task. Use your chart to create an algorithm to determine the most efficient path.", "Required": False},

    # Whittling (5 requirements)
    {"Req_ID": "Whittling.1", "Adventure": "Whittling", "Requirement_Description": "Read, understand, and promise to follow the 'Cub Scout Knife Safety Rules.'", "Required": False},
    {"Req_ID": "Whittling.2", "Adventure": "Whittling", "Requirement_Description": "Demonstrate the knife safety circle.", "Required": False},
    {"Req_ID": "Whittling.3", "Adventure": "Whittling", "Requirement_Description": "Demonstrate that you know how to care for and use a pocketknife safely. Show proper hand position when using a pocketknife.", "Required": False},
    {"Req_ID": "Whittling.4", "Adventure": "Whittling", "Requirement_Description": "Make a carved hiking stick.", "Required": False},
    {"Req_ID": "Whittling.5", "Adventure": "Whittling", "Requirement_Description": "Earn your Whittling Chip card.", "Required": False},
]

# Webelos Scout Requirements (4th Grade)
WEBELOS_REQUIREMENTS = [
    # Required Adventures (6 total)
    # Bobcat Adventure (7 requirements)
    {"Req_ID": "BobcatWebelos.1", "Adventure": "Bobcat Adventure", "Requirement_Description": "Get to know members of your den.", "Required": True},
    {"Req_ID": "BobcatWebelos.2", "Adventure": "Bobcat Adventure", "Requirement_Description": "Recite the Scout Oath and the Scout Law with your den and den leader. Describe the three points of the Scout Oath.", "Required": True},
    {"Req_ID": "BobcatWebelos.3", "Adventure": "Bobcat Adventure", "Requirement_Description": "Learn about the Scout Law.", "Required": True},
    {"Req_ID": "BobcatWebelos.4", "Adventure": "Bobcat Adventure", "Requirement_Description": "With your den create a den Code of Conduct.", "Required": True},
    {"Req_ID": "BobcatWebelos.5", "Adventure": "Bobcat Adventure", "Requirement_Description": "Learn about the denner position and responsibilities.", "Required": True},
    {"Req_ID": "BobcatWebelos.6", "Adventure": "Bobcat Adventure", "Requirement_Description": "Demonstrate the Cub Scout sign, Cub Scout salute and Cub Scout handshake. Show how each is used.", "Required": True},
    {"Req_ID": "BobcatWebelos.7", "Adventure": "Bobcat Adventure", "Requirement_Description": "At home, with your parent or legal guardian do the activities in the booklet 'How to Protect Your Children from Child Abuse: A Parent's Guide.'", "Required": True},

    # Stronger, Faster, Higher (5 requirements)
    {"Req_ID": "StrongerFasterHigher.1", "Adventure": "Stronger, Faster, Higher", "Requirement_Description": "With your den or family, plan, cook, and eat a balanced meal.", "Required": True},
    {"Req_ID": "StrongerFasterHigher.2", "Adventure": "Stronger, Faster, Higher", "Requirement_Description": "Be active for 30 minutes with your den or at least one other person in a way that includes both stretching and moving.", "Required": True},
    {"Req_ID": "StrongerFasterHigher.3", "Adventure": "Stronger, Faster, Higher", "Requirement_Description": "Be active for 15 minutes doing personal exercises that boost your heart rate, use your muscles, and work on flexibility.", "Required": True},
    {"Req_ID": "StrongerFasterHigher.4", "Adventure": "Stronger, Faster, Higher", "Requirement_Description": "Do a relaxing activity for 10 minutes.", "Required": True},
    {"Req_ID": "StrongerFasterHigher.5", "Adventure": "Stronger, Faster, Higher", "Requirement_Description": "Review your Scouting America Annual Health and Medical Record with your parent or legal guardian. Discuss your ability to participate in den and pack activities.", "Required": True},

    # My Safety (4 requirements)
    {"Req_ID": "MySafety.1", "Adventure": "My Safety", "Requirement_Description": "With permission from your parent or legal guardian, watch the Protect Yourself Rules video for the Webelos rank.", "Required": True},
    {"Req_ID": "MySafety.2", "Adventure": "My Safety", "Requirement_Description": "Identify items in your house that are hazardous and make sure they are stored properly. Identify on the package where it describes what to do if someone is accidentally exposed to them.", "Required": True},
    {"Req_ID": "MySafety.3", "Adventure": "My Safety", "Requirement_Description": "Identify ways you and your family keep your home or your meeting space safe.", "Required": True},
    {"Req_ID": "MySafety.4", "Adventure": "My Safety", "Requirement_Description": "Complete the Be Prepared for Natural Events worksheet. Complete a worksheet for at least two natural events most likely to happen near where you live.", "Required": True},

    # My Family (4 requirements)
    {"Req_ID": "MyFamily.1", "Adventure": "My Family", "Requirement_Description": "With your parent or legal guardian, talk about your family's faith traditions. Identify three holidays or celebrations that are part of your family's faith traditions. Make a craft, work of art, or a food item that is part of your family's faith traditions.", "Required": True},
    {"Req_ID": "MyFamily.2", "Adventure": "My Family", "Requirement_Description": "Carry out an act of kindness.", "Required": True},
    {"Req_ID": "MyFamily.3", "Adventure": "My Family", "Requirement_Description": "With your parent or legal guardian identify a religion or faith that is different from your own. Identify two things that it has in common with your family's beliefs.", "Required": True},
    {"Req_ID": "MyFamily.4", "Adventure": "My Family", "Requirement_Description": "Discuss with your parent or legal guardian what it means to be reverent. Tell how you practice being reverent in your daily life.", "Required": True},

    # My Community (4 requirements)
    {"Req_ID": "MyCommunity.1", "Adventure": "My Community", "Requirement_Description": "Learn about majority and plurality types of voting.", "Required": True},
    {"Req_ID": "MyCommunity.2", "Adventure": "My Community", "Requirement_Description": "Speak with someone who is elected to their position. Discover the type of voting that was used to elect them and why.", "Required": True},
    {"Req_ID": "MyCommunity.3", "Adventure": "My Community", "Requirement_Description": "Choose a federal law and create a timeline of the history of the law. Include the involvement of the 3 branches of government.", "Required": True},
    {"Req_ID": "MyCommunity.4", "Adventure": "My Community", "Requirement_Description": "Participate in a service project.", "Required": True},

    # Webelos Walkabout (7 requirements)
    {"Req_ID": "WebelosWalkabout.1", "Adventure": "Webelos Walkabout", "Requirement_Description": "Prepare for a 2-mile walk outside. Gather your Cub Scout Six Essentials and weather appropriate clothing and shoes.", "Required": True},
    {"Req_ID": "WebelosWalkabout.2", "Adventure": "Webelos Walkabout", "Requirement_Description": "Plan a 2-mile route for your walk.", "Required": True},
    {"Req_ID": "WebelosWalkabout.3", "Adventure": "Webelos Walkabout", "Requirement_Description": "Check the weather forecast for the time of your planned 2-mile walk.", "Required": True},
    {"Req_ID": "WebelosWalkabout.4", "Adventure": "Webelos Walkabout", "Requirement_Description": "Review the four points of Scouting America SAFE Checklist and how you will apply them on your 2-mile walk.", "Required": True},
    {"Req_ID": "WebelosWalkabout.5", "Adventure": "Webelos Walkabout", "Requirement_Description": "Demonstrate first aid for each of the following events that could occur on your 2-mile walk: blister, sprained ankle, sunburn, dehydration and heat related illness.", "Required": True},
    {"Req_ID": "WebelosWalkabout.6", "Adventure": "Webelos Walkabout", "Requirement_Description": "With your den, pack, or family, go on your 2-mile walk while practicing the Leave No Trace Principles for Kids and Outdoor Code.", "Required": True},
    {"Req_ID": "WebelosWalkabout.7", "Adventure": "Webelos Walkabout", "Requirement_Description": "After your 2-mile walk, discuss with your den what went well and what you would do differently next time.", "Required": True},

    # Elective Adventures (Complete any 2)
    # Aquanaut (6 requirements)
    {"Req_ID": "Aquanaut.1", "Adventure": "Aquanaut", "Requirement_Description": "State the safety precautions you need to take before doing any swimming activity.", "Required": False},
    {"Req_ID": "Aquanaut.2", "Adventure": "Aquanaut", "Requirement_Description": "Explain the meaning of 'order of rescue' and demonstrate the reach and throw rescue techniques from land.", "Required": False},
    {"Req_ID": "Aquanaut.3", "Adventure": "Aquanaut", "Requirement_Description": "Learn how to prevent and treat hypothermia.", "Required": False},
    {"Req_ID": "Aquanaut.4", "Adventure": "Aquanaut", "Requirement_Description": "Attempt to tread water.", "Required": False},
    {"Req_ID": "Aquanaut.5", "Adventure": "Aquanaut", "Requirement_Description": "Attempt Scouting America swimmer test.", "Required": False},
    {"Req_ID": "Aquanaut.6", "Adventure": "Aquanaut", "Requirement_Description": "Have 30 minutes, or more, of free swim time where you practice the Buddy System and stay within your ability group. The qualified adult supervision should conduct at least three buddy checks per half hour swimming.", "Required": False},

    # Art Explosion (4 requirements)
    {"Req_ID": "ArtExplosion.1", "Adventure": "Art Explosion", "Requirement_Description": "Create a piece of art by exploring drawing techniques using pencils.", "Required": False},
    {"Req_ID": "ArtExplosion.2", "Adventure": "Art Explosion", "Requirement_Description": "Using a digital image, explore the effect of filters by changing an image using different editing or in-camera techniques.", "Required": False},
    {"Req_ID": "ArtExplosion.3", "Adventure": "Art Explosion", "Requirement_Description": "Create a piece of art using paint as your medium.", "Required": False},
    {"Req_ID": "ArtExplosion.4", "Adventure": "Art Explosion", "Requirement_Description": "Create a piece of art combining at least two media.", "Required": False},

    # Aware and Care (4 requirements)
    {"Req_ID": "AwareAndCare.1", "Adventure": "Aware and Care", "Requirement_Description": "Do an activity that shows the challenges of a being visually impaired.", "Required": False},
    {"Req_ID": "AwareAndCare.2", "Adventure": "Aware and Care", "Requirement_Description": "Do an activity that shows the challenges of being hearing impaired.", "Required": False},
    {"Req_ID": "AwareAndCare.3", "Adventure": "Aware and Care", "Requirement_Description": "Explore barriers to access.", "Required": False},
    {"Req_ID": "AwareAndCare.4", "Adventure": "Aware and Care", "Requirement_Description": "Meet someone who has a disability or someone who works with people with disabilities about what obstacles they must overcome and how they do it.", "Required": False},

    # Build It (4 requirements)
    {"Req_ID": "BuildIt.1", "Adventure": "Build It", "Requirement_Description": "Learn about some basic tools and the proper use of each tool. Learn about and understand the need for safety when you work with tools.", "Required": False},
    {"Req_ID": "BuildIt.2", "Adventure": "Build It", "Requirement_Description": "Demonstrate how to check for plumb, level, and square when building.", "Required": False},
    {"Req_ID": "BuildIt.3", "Adventure": "Build It", "Requirement_Description": "With the guidance of your Webelos den leader, parent, or legal guardian, select a carpentry project that requires it to be either plumb, level, and/or square. Create a list of materials and tools you will need to complete the project.", "Required": False},
    {"Req_ID": "BuildIt.4", "Adventure": "Build It", "Requirement_Description": "Build your carpentry project.", "Required": False},

    # Catch the Big One (7 requirements)
    {"Req_ID": "CatchTheBigOne.1", "Adventure": "Catch the Big One", "Requirement_Description": "Make a plan to go fishing. Determine where you will go and what type of fish you plan to catch. All of the following requirements are to be completed based on your choice.", "Required": False},
    {"Req_ID": "CatchTheBigOne.2", "Adventure": "Catch the Big One", "Requirement_Description": "Use Scouting America SAFE Checklist to plan what you need for your fishing experience.", "Required": False},
    {"Req_ID": "CatchTheBigOne.3", "Adventure": "Catch the Big One", "Requirement_Description": "Describe the environment where the fish might be found.", "Required": False},
    {"Req_ID": "CatchTheBigOne.4", "Adventure": "Catch the Big One", "Requirement_Description": "Make a list of the equipment and materials you will need to fish.", "Required": False},
    {"Req_ID": "CatchTheBigOne.5", "Adventure": "Catch the Big One", "Requirement_Description": "Determine the best type of knot to tie your hook to your line and tie it.", "Required": False},
    {"Req_ID": "CatchTheBigOne.6", "Adventure": "Catch the Big One", "Requirement_Description": "Choose the appropriate type of fishing rod and tackle you will be using. Have an adult review your gear.", "Required": False},
    {"Req_ID": "CatchTheBigOne.7", "Adventure": "Catch the Big One", "Requirement_Description": "Using what you have learned about fish and fishing equipment, spend at least one hour fishing following local guidelines and regulations.", "Required": False},

    # Champions for Nature Webelos (6 requirements)
    {"Req_ID": "ChampionsNatureWebelos.1", "Adventure": "Champions for Nature Webelos", "Requirement_Description": "Discover the four components that make up a habitat: food, water, shelter, space.", "Required": False},
    {"Req_ID": "ChampionsNatureWebelos.2", "Adventure": "Champions for Nature Webelos", "Requirement_Description": "Pick an animal that is currently threatened or endangered to complete requirements 3, 4, and 5.", "Required": False},
    {"Req_ID": "ChampionsNatureWebelos.3", "Adventure": "Champions for Nature Webelos", "Requirement_Description": "Identify the characteristics that classify an animal as a threatened or endangered species.", "Required": False},
    {"Req_ID": "ChampionsNatureWebelos.4", "Adventure": "Champions for Nature Webelos", "Requirement_Description": "Explore what caused this animal to be threatened or endangered.", "Required": False},
    {"Req_ID": "ChampionsNatureWebelos.5", "Adventure": "Champions for Nature Webelos", "Requirement_Description": "Research what is currently being done to protect the animal.", "Required": False},
    {"Req_ID": "ChampionsNatureWebelos.6", "Adventure": "Champions for Nature Webelos", "Requirement_Description": "Participate in a conservation service project.", "Required": False},

    # Chef's Knife (4 requirements)
    {"Req_ID": "ChefsKnife.1", "Adventure": "Chef's Knife", "Requirement_Description": "Read, understand, and promise to follow the 'Cub Scout Knife Safety Rules.'", "Required": False},
    {"Req_ID": "ChefsKnife.2", "Adventure": "Chef's Knife", "Requirement_Description": "Demonstrate the knife safety circle.", "Required": False},
    {"Req_ID": "ChefsKnife.3", "Adventure": "Chef's Knife", "Requirement_Description": "Demonstrate that you know how to care for and use a kitchen knife safely.", "Required": False},
    {"Req_ID": "ChefsKnife.4", "Adventure": "Chef's Knife", "Requirement_Description": "Choose the correct cooking knife and demonstrate how to properly slice, dice, and mince.", "Required": False},

    # Earth Rocks (4 requirements)
    {"Req_ID": "EarthRocks.1", "Adventure": "Earth Rocks", "Requirement_Description": "Examine the three types of rocks, sedimentary, igneous, and metamorphic.", "Required": False},
    {"Req_ID": "EarthRocks.2", "Adventure": "Earth Rocks", "Requirement_Description": "Find a rock, safely break it apart and examine it.", "Required": False},
    {"Req_ID": "EarthRocks.3", "Adventure": "Earth Rocks", "Requirement_Description": "Make a mineral test kit and test minerals according to the Mohs scale of mineral hardness. Using the rock cycle chart or one like it, discuss how hardness determines which materials can be used in homes, in landscapes, or for recreation.", "Required": False},
    {"Req_ID": "EarthRocks.4", "Adventure": "Earth Rocks", "Requirement_Description": "Grow a crystal.", "Required": False},

    # Let's Camp Webelos (9 requirements)
    {"Req_ID": "LetsCampWebelos.1", "Adventure": "Let's Camp Webelos", "Requirement_Description": "With your den, pack, or family, plan and participate in a campout.", "Required": False},
    {"Req_ID": "LetsCampWebelos.2", "Adventure": "Let's Camp Webelos", "Requirement_Description": "Upon arrival at the campground, determine where to set up a tent.", "Required": False},
    {"Req_ID": "LetsCampWebelos.3", "Adventure": "Let's Camp Webelos", "Requirement_Description": "Set up your tent without help from an adult.", "Required": False},
    {"Req_ID": "LetsCampWebelos.4", "Adventure": "Let's Camp Webelos", "Requirement_Description": "Identify a potential weather hazard that could occur in your area. Determine the action you will take if you experience the weather hazard during the campout.", "Required": False},
    {"Req_ID": "LetsCampWebelos.5", "Adventure": "Let's Camp Webelos", "Requirement_Description": "Show how to tie a bowline. Explain when this knot should be used and why.", "Required": False},
    {"Req_ID": "LetsCampWebelos.6", "Adventure": "Let's Camp Webelos", "Requirement_Description": "Know the fire safety rules. Using those rules, locate a safe area to build a campfire.", "Required": False},
    {"Req_ID": "LetsCampWebelos.7", "Adventure": "Let's Camp Webelos", "Requirement_Description": "Using tinder, kindling, and fuel wood, properly build a teepee fire lay. If circumstances permit, and there is no local restriction on fires, show how to safely light the fire while under adult supervision. After allowing the fire to burn safely, extinguish the flames with minimal impact to the fire site.", "Required": False},
    {"Req_ID": "LetsCampWebelos.8", "Adventure": "Let's Camp Webelos", "Requirement_Description": "Recite the Outdoor Code and Leave No Trace Principles for Kids from Memory.", "Required": False},
    {"Req_ID": "LetsCampWebelos.9", "Adventure": "Let's Camp Webelos", "Requirement_Description": "After your campout, share the things you did to follow the Outdoor Code and Leave No Trace Principles for Kids with your den or family.", "Required": False},

    # Math on the Trail (3 requirements)
    {"Req_ID": "MathOnTheTrail.1", "Adventure": "Math on the Trail", "Requirement_Description": "Determine your walking pace by walking ¼ mile. Make a projection on how long it would take you to walk 2 miles.", "Required": False},
    {"Req_ID": "MathOnTheTrail.2", "Adventure": "Math on the Trail", "Requirement_Description": "Walk 2 miles and record the time it took you to complete the two miles.", "Required": False},
    {"Req_ID": "MathOnTheTrail.3", "Adventure": "Math on the Trail", "Requirement_Description": "Make a projection on how long it would take you to hike a 20-mile trail over two days. List all the factors to consider for your projection.", "Required": False},

    # Modular Design (6 requirements)
    {"Req_ID": "ModularDesign.1", "Adventure": "Modular Design", "Requirement_Description": "Learn what modular design is and identify three things that use modular design in their construction.", "Required": False},
    {"Req_ID": "ModularDesign.2", "Adventure": "Modular Design", "Requirement_Description": "Using modular-based building pieces, build a model without a set of instructions.", "Required": False},
    {"Req_ID": "ModularDesign.3", "Adventure": "Modular Design", "Requirement_Description": "Using the model made in requirement 2, create a set of step-by-step instructions on how to make your model.", "Required": False},
    {"Req_ID": "ModularDesign.4", "Adventure": "Modular Design", "Requirement_Description": "Have someone make your model using your instructions.", "Required": False},
    {"Req_ID": "ModularDesign.5", "Adventure": "Modular Design", "Requirement_Description": "Using the same modular pieces used in requirement 2, build another model of something different.", "Required": False},
    {"Req_ID": "ModularDesign.6", "Adventure": "Modular Design", "Requirement_Description": "With your parent or legal guardian's permission, watch a video demonstrating how something was built using modular design.", "Required": False},

    # Paddle Onward (9 requirements)
    {"Req_ID": "PaddleOnward.1", "Adventure": "Paddle Onward", "Requirement_Description": "Before attempting requirements 5, 6, 7, 8 and 9 for this Adventure, you must pass Scouting America swimmer test.", "Required": False},
    {"Req_ID": "PaddleOnward.2", "Adventure": "Paddle Onward", "Requirement_Description": "Pick a paddle craft for which to complete all requirements: canoe, kayak, or stand-up paddleboard.", "Required": False},
    {"Req_ID": "PaddleOnward.3", "Adventure": "Paddle Onward", "Requirement_Description": "Review Safety Afloat.", "Required": False},
    {"Req_ID": "PaddleOnward.4", "Adventure": "Paddle Onward", "Requirement_Description": "Demonstrate how to choose and properly wear a life jacket that is the correct size.", "Required": False},
    {"Req_ID": "PaddleOnward.5", "Adventure": "Paddle Onward", "Requirement_Description": "Jump feet first into water over your head while wearing a life jacket. Then swim 25 feet wearing the life jacket.", "Required": False},
    {"Req_ID": "PaddleOnward.6", "Adventure": "Paddle Onward", "Requirement_Description": "Demonstrate how to enter and exit a canoe, kayak, or stand-up paddleboard safely.", "Required": False},
    {"Req_ID": "PaddleOnward.7", "Adventure": "Paddle Onward", "Requirement_Description": "Discuss what to do if your canoe or kayak tips over or you fall off your stand-up paddleboard.", "Required": False},
    {"Req_ID": "PaddleOnward.8", "Adventure": "Paddle Onward", "Requirement_Description": "Learn how to pick a paddle that is the right size for you. Explore how the paddle craft responds to moving the paddle.", "Required": False},
    {"Req_ID": "PaddleOnward.9", "Adventure": "Paddle Onward", "Requirement_Description": "Have 30 minutes, or more, of canoe, kayak, or stand-up paddleboard paddle time.", "Required": False},

    # Pedal Away (6 requirements)
    {"Req_ID": "PedalAway.1", "Adventure": "Pedal Away", "Requirement_Description": "Decide on gear and supplies you should bring for a long bike ride.", "Required": False},
    {"Req_ID": "PedalAway.2", "Adventure": "Pedal Away", "Requirement_Description": "Discover how multi-gear bicycles work and how they benefit a rider.", "Required": False},
    {"Req_ID": "PedalAway.3", "Adventure": "Pedal Away", "Requirement_Description": "Practice how to lubricate a chain.", "Required": False},
    {"Req_ID": "PedalAway.4", "Adventure": "Pedal Away", "Requirement_Description": "Pick a bicycle lock that you will use. Demonstrate how it locks and unlocks, how it secures your bicycle, and how you carry it while you are riding your bicycle.", "Required": False},
    {"Req_ID": "PedalAway.5", "Adventure": "Pedal Away", "Requirement_Description": "With your family, den, or pack, use a map and plan a bicycle ride that is at least 5 miles.", "Required": False},
    {"Req_ID": "PedalAway.6", "Adventure": "Pedal Away", "Requirement_Description": "With your den, pack, or family and using the buddy system, go on a bicycle ride that is a minimum of 5 miles.", "Required": False},

    # Race Time Webelos (5 requirements)
    {"Req_ID": "RaceTimeWebelos.1", "Adventure": "Race Time Webelos", "Requirement_Description": "With an adult, build either a Pinewood Derby car or a Raingutter Regatta boat.", "Required": False},
    {"Req_ID": "RaceTimeWebelos.2", "Adventure": "Race Time Webelos", "Requirement_Description": "Learn the rules of the race for the vehicle chosen in requirement 1.", "Required": False},
    {"Req_ID": "RaceTimeWebelos.3", "Adventure": "Race Time Webelos", "Requirement_Description": "Explore the properties of friction and how it impacts your chosen vehicle.", "Required": False},
    {"Req_ID": "RaceTimeWebelos.4", "Adventure": "Race Time Webelos", "Requirement_Description": "Before the race, discuss with your den how you will demonstrate good sportsmanship during the race.", "Required": False},
    {"Req_ID": "RaceTimeWebelos.5", "Adventure": "Race Time Webelos", "Requirement_Description": "Participate in a Pinewood Derby or a Raingutter Regatta.", "Required": False},

    # Summertime Fun Webelos (1 requirement)
    {"Req_ID": "SummertimeFunWebelos.1", "Adventure": "Summertime Fun Webelos", "Requirement_Description": "Anytime during May through August participate in a total of three Cub Scout activities.", "Required": False},

    # Tech on the Trail (4 requirements)
    {"Req_ID": "TechOnTheTrail.1", "Adventure": "Tech on the Trail", "Requirement_Description": "Discuss how technology can help keep you safe in the outdoors.", "Required": False},
    {"Req_ID": "TechOnTheTrail.2", "Adventure": "Tech on the Trail", "Requirement_Description": "Explore Global Positioning Satellite and how to use it.", "Required": False},
    {"Req_ID": "TechOnTheTrail.3", "Adventure": "Tech on the Trail", "Requirement_Description": "With an adult, choose an online mapping program tool and plan a 2-mile trek.", "Required": False},
    {"Req_ID": "TechOnTheTrail.4", "Adventure": "Tech on the Trail", "Requirement_Description": "Take your 2-mile trek.", "Required": False},

    # Yo-yo (7 requirements)
    {"Req_ID": "YoYo.1", "Adventure": "Yo-yo", "Requirement_Description": "Learn the safety rules of using a yo-yo and always follow them.", "Required": False},
    {"Req_ID": "YoYo.2", "Adventure": "Yo-yo", "Requirement_Description": "Discover how to find the proper yo-yo string length for you.", "Required": False},
    {"Req_ID": "YoYo.3", "Adventure": "Yo-yo", "Requirement_Description": "Explain why it is important to have the correct string length and to be in the right location before throwing a yo-yo.", "Required": False},
    {"Req_ID": "YoYo.4", "Adventure": "Yo-yo", "Requirement_Description": "Demonstrate how to properly string a yo-yo and how to create a slip knot.", "Required": False},
    {"Req_ID": "YoYo.5", "Adventure": "Yo-yo", "Requirement_Description": "Conduct the pendulum experiment with a yo-yo. Explain what happens to the yo-yo when the string is longer.", "Required": False},
    {"Req_ID": "YoYo.6", "Adventure": "Yo-yo", "Requirement_Description": "Show that you can properly wind a yo-yo.", "Required": False},
    {"Req_ID": "YoYo.7", "Adventure": "Yo-yo", "Requirement_Description": "Attempt each of the following: gravity pull, sleeper, breakaway.", "Required": False},
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
