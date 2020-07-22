import sys
import pandas as pd

sys.path.append(".")

from data_extractor import DataExtractor

'''
Janet_Evanovich = [
    [207, 'https://play.google.com/store/books/details/Janet_Evanovich_One_For_The_Money?id=iuc9opwJ7awC'],
    [996, 'https://play.google.com/store/books/details/Janet_Evanovich_Three_To_Get_Deadly?id=EXl6DW2h0iYC'],
    [1067, 'https://play.google.com/store/books/details/Janet_Evanovich_Four_to_Score?id=eXq8H6APWAYC'],
    [1226, 'https://play.google.com/store/books/details/Janet_Evanovich_Seven_Up?id=cRBrmBYjjGQC'],
    [1390, 'https://play.google.com/store/books/details/Janet_Evanovich_Eleven_on_Top?id=q1ys6WUmVmoC'],
    [1606, 'https://play.google.com/store/books/details/Janet_Evanovich_Ten_Big_Ones?id=Kps4QJ_W4iAC'],
    [1694, 'https://play.google.com/store/books/details/Janet_Evanovich_Lean_Mean_Thirteen?id=QiIITzhbbkcC'],
    [1811, 'https://play.google.com/store/books/details/Janet_Evanovich_Visions_of_Sugar_Plums?id=f4UK7BCl1usC'],
    [1821, 'https://play.google.com/store/books/details/Janet_Evanovich_Fearless_Fourteen?id=6u_VRZHH4GIC'],
    [1959, 'https://play.google.com/store/books/details/Janet_Evanovich_Finger_Lickin_Fifteen?id=O7-V90OQVQsC'],
    [2800, 'https://play.google.com/store/books/details/Janet_Evanovich_Takedown_Twenty?id=3QouC5_MJnQC'],
    [3025, 'https://play.google.com/store/books/details/Janet_Evanovich_Plum_Lovin?id=ZUXXwSQ6OnoC'],
    [3113, 'https://play.google.com/store/books/details/Janet_Evanovich_Wicked_Appetite?id=NSK9cDNJX8AC'],
    [3515, 'https://play.google.com/store/books/details/Janet_Evanovich_Plum_Lucky?id=oUwkWC0ZH_oC'],
    [6132, 'https://play.google.com/store/books/details/Janet_Evanovich_Motor_Mouth?id=hx43bSGFUYAC']
   ]

laurell_k_hamilton = [
            [1553, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Circus_of_the_Damned?id=7r2m6JSaHOoC"],
            [2090, "https://play.google.com/store/books/details/Laurell_K_Hamilton_The_Laughing_Corpse?id=KJBovRMFy4QC"],
            [2341, "https://play.google.com/store/books/details/Laurell_K_Hamilton_The_Killing_Dance?id=CTxn2lZ7qwkC"],
            [2549, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Blue_Moon?id=DYIulDNq9K0C"],
            [2550, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Burnt_Offerings?id=hL5t6pi9CawC"],
            [3510, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Cerulean_Sins?id=nWHVhGo5GW4C"],
            [3874, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Micah?id=x7aL5KOFkw0C"],
            [3990, "https://play.google.com/store/books/details/Laurell_K_Hamilton_The_Harlequin?id=dy-XlEFgDHQC"],
            [4425, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Blood_Noir?id=UAEe2NNEnMMC"],
            [4656, "https://play.google.com/store/books/details/Laurell_K_Hamilton_A_Caress_of_Twilight?id=oTF82eOdgUIC"],
            [4867, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Skin_Trade?id=x1Jw4XOoV98C"],
            [5295, "https://play.google.com/store/books/details/Laurell_K_Hamilton_A_Stroke_of_Midnight?id=pESaw8Nwi-MC"],
            [5370, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Bullet?id=wmgF8XJf4l4C"],
            [5410, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Flirt?id=fiBhVEiOFw0C"],
            [5609, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Mistral_s_Kiss?id=fLddEo6JMMQC"],
            [6080, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Swallowing_Darkness?id=SHpfEF6vPjMC"],
            [8398, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Strange_Candy?id=cJjssstBM7wC"],
            [8851, "https://play.google.com/store/books/details/Laurell_K_Hamilton_Affliction?id=y9bFBrmMVIgC"]
        ]

David_Baldacci = [
    [1831, "https://play.google.com/store/books/details/David_Baldacci_The_Innocent?id=61bLpirAu8MC"],
    [2180, "https://play.google.com/store/books/details/David_Baldacci_Zero_Day?id=l-RAJU8VO_UC"],
    [2383, "https://play.google.com/store/books/details/David_Baldacci_Split_Second?id=tcmC1BEkbnUC"],
    [2842, "https://play.google.com/store/books/details/David_Baldacci_Divine_Justice?id=8tha6mtCbBsC"],
    [3050, "https://play.google.com/store/books/details/David_Baldacci_The_Sixth_Man?id=T1pXtdLwJjMC"],
    [3357, "https://play.google.com/store/books/details/David_Baldacci_The_Collectors?id=bx53R7Q0HJUC"],
    [3945, "https://play.google.com/store/books/details/David_Baldacci_Total_Control?id=dNTvIxPbG40C"],
	[4040, "https://play.google.com/store/books/details/David_Baldacci_The_Simple_Truth?id=YnMGnsO6740C"],
	[4294, "https://play.google.com/store/books/details/David_Baldacci_Hour_Game?id=q72F-CZOER4C"],
	[4463, "https://play.google.com/store/books/details/David_Baldacci_First_Family?id=9JW_MaYJB9wC"],
	[5941, "https://play.google.com/store/books/details/David_Baldacci_Deliver_Us_from_Evil?id=529dtmE_FgMC"],
	[6028, "https://play.google.com/store/books/details/David_Baldacci_One_Summer?id=uq86C-khIa4C"]
]

Dean_Koontz = [
    [1709, "https://play.google.com/store/books/details/Dean_Koontz_Forever_Odd?id=JECA8s4s12YC"],
    [1719, "https://play.google.com/store/books/details/Dean_Koontz_Phantoms?id=7-gcMsbRhHgC"],
    [2657, "https://play.google.com/store/books/details/Dean_Koontz_False_Memory?id=6LZ--eGLk8IC"],
    [3374, "https://play.google.com/store/books/details/Dean_Koontz_The_Taking?id=v3QwImAObqwC"],
    [3804, "https://play.google.com/store/books/details/Dean_Koontz_Whispers?id=NyZ7Wp2jkqMC"],
    [4085, "https://play.google.com/store/books/details/Dean_Koontz_The_Bad_Place?id=t-WRQ9ofWDMC"],
    [4387, "https://play.google.com/store/books/details/Dean_Koontz_From_the_Corner_of_His_Eye?id=jrn0hhqWdNAC"],
    [4795, "https://play.google.com/store/books/details/Dean_Koontz_Night_Chills?id=7lNHu1199SwC"],
    [6539, "https://play.google.com/store/books/details/Dean_Koontz_One_Door_Away_from_Heaven?id=_klU1t2uqzEC"],
    [6833, "https://play.google.com/store/books/details/Dean_Koontz_Darkfall?id=ynl8DvOJRSkC"],
    [8444, "https://play.google.com/store/books/details/Dean_Koontz_Relentless?id=sNgW645XIAkC"]
]

Nora_Roberts = [
    [1751,    "https://play.google.com/store/books/details/Nora_Roberts_Born_in_Fire?id=pG9WvfN4HrEC"],
    [1966,    "https://play.google.com/store/books/details/Nora_Roberts_Jewels_of_the_Sun?id=UtQmfEUvceQC"],
    [2159,    "https://play.google.com/store/books/details/Nora_Roberts_Sea_Swept?id=7z1J2RUEVPUC"],
    [3213,    "https://play.google.com/store/books/details/Nora_Roberts_Angels_Fall?id=14XgSYyeLB0C"],
    [4172,    "https://play.google.com/store/books/details/Nora_Roberts_Black_Hills?id=KOJ6JcKqIbQC"],
    [4308,    "https://play.google.com/store/books/details/Nora_Roberts_Red_Lily?id=1ejJBbmGtvAC"],
    [4619,    "https://play.google.com/store/books/details/Nora_Roberts_Key_Of_Valor?id=s2kTaPe9xOEC"],
    [4871,    "https://play.google.com/store/books/details/Nora_Roberts_Born_in_Ice?id=ZzswoJu8c_QC"],
    [4957,   "https://play.google.com/store/books/details/Nora_Roberts_Shadow_Spell?id=45wlAgAAQBAJ"],
    [5158,    "https://play.google.com/store/books/details/Nora_Roberts_Tears_of_the_Moon?id=u5InN3sw5CYC"],
    [5431,    "https://play.google.com/store/books/details/Nora_Roberts_Chesapeake_Blue?id=yPj6Jj2YRPkC"],
    [5522,    "https://play.google.com/store/books/details/Nora_Roberts_Rising_Tides?id=fy2YxvOf_EQC"],
    [5600,    "https://play.google.com/store/books/details/Nora_Roberts_The_Hollow?id=CEy3Hml6dvoC"],
    [5748,    "https://play.google.com/store/books/details/Nora_Roberts_Heart_of_the_Sea?id=uCgqpXqxUzAC"],
    [5871,    "https://play.google.com/store/books/details/Nora_Roberts_The_Pagan_Stone?id=0HsyH6p0xEsC"],
    [6267,    "https://play.google.com/store/books/details/Nora_Roberts_The_Villa?id=737KtjONT5kC"],
    [7704,    "https://play.google.com/store/books/details/Nora_Roberts_Holding_the_Dream?id=dCI2F7MTmNgC"],
    [7982,    "https://play.google.com/store/books/details/Nora_Roberts_Hidden_Riches?id=5MRhtNvR8AgC"],
    [9493,    "https://play.google.com/store/books/details/Nora_Roberts_The_Reef?id=LhUNoKbgk1gC"]
]

Orson_Scott_Card = [
    [492,	"https://play.google.com/store/books/details/Orson_Scott_Card_Speaker_for_the_Dead?id=JJ8ubAShaQYC"],
    [1646,	"https://play.google.com/store/books/details/Orson_Scott_Card_Shadow_of_the_Hegemon?id=8hCrVKGLQMgC"],
    [2900,	"https://play.google.com/store/books/details/Orson_Scott_Card_Ender_in_Exile?id=Oa8W1lM7dp0C"],
    [5288,	"https://play.google.com/store/books/details/Orson_Scott_Card_The_Lost_Gate?id=rzXH0wnmo0IC"],
    [6490,	"https://play.google.com/store/books/details/Orson_Scott_Card_Pathfinder?id=xU4EOc9zmCMC"],
    [6701,	"https://play.google.com/store/books/details/Orson_Scott_Card_Red_Prophet?id=O4uh6XaBu-IC"],
    [7490,	"https://play.google.com/store/books/details/Orson_Scott_Card_Prentice_Alvin?id=r7zhdBLKWXcC"],
    [8413,	"https://play.google.com/store/books/details/Orson_Scott_Card_Alvin_Journeyman?id=DA9908OBR3EC"],
    [8944,	"https://play.google.com/store/books/details/Orson_Scott_Card_Pastwatch?id=6-Q2gmxilJ8C"],
    [9643,	"https://play.google.com/store/books/details/Orson_Scott_Card_The_Gate_Thief?id=1nmdgTgNA0cC"],
    [9723,	"https://play.google.com/store/books/details/Orson_Scott_Card_A_War_of_Gifts?id=gfSi2-2CRqoC"]
]

Nicholas_Sparks = [
    [107, "A Walk to Remember"],
    [152, "Dear John"],
    [286, "The Lucky One"],
    [420, "Message in a Bottle"],
    [552,  "The Rescue"],
    [571,  "The Guardian"],
    [686,	"The Wedding"],
    [716,	"The Choice"],
    [821,	"The Best of Me"],
    [1414,	"True Believer"],
    [1459,	"At First Sight"]
]

Stephen_King = [
    [176, "It"],
    [232, "The Gunslinger"],
    [609, "Cell"],
    [670, "The Dead Zone"],
    [703, "Bag of Bones"],
    [953, "The Dark Tower"],
    [1339,	"The Mist"],
    [1347,	"Revival"],
    [1360,	"Duma Key"],
    [1576,	"Full Dark, No Stars"],
    [2155,	"From a Buick 8"]
]

James_Patterson = [
	[336, "https://play.google.com/store/books/details/James_Patterson_1st_to_Die?id=DY1adEvMVRAC"],
	[1351, "https://play.google.com/store/books/details/James_Patterson_School_s_Out_Forever?id=vdVUeFYSHJYC"],
	[1535, "https://play.google.com/store/books/details/James_Patterson_Saving_the_World_and_Other_Extreme?id=YRUh6EtxyOYC"],
	[1746, "https://play.google.com/store/books/details/James_Patterson_Hide_and_Seek?id=5olfJ_vDDDwC"],
	[2282, "https://play.google.com/store/books/details/James_Patterson_Max?id=A9L1hC0vle8C"],
	[2381, "https://play.google.com/store/books/details/James_Patterson_The_Final_Warning?id=lR5HTs4ggGYC"],
	[2398, "https://play.google.com/store/books/details/James_Patterson_Roses_Are_Red?id=Znt-ecoo_3wC"],
	[2737, "https://play.google.com/store/books/details/James_Patterson_The_Big_Bad_Wolf?id=cSeFNUfRaewC"],
	[2974, "https://play.google.com/store/books/details/James_Patterson_Angel?id=EGRLRfGTpF8C"],
	[3066, "https://play.google.com/store/books/details/James_Patterson_Four_Blind_Mice?id=GORmiUWSZYkC"],
	[3223, "https://play.google.com/store/books/details/James_Patterson_London_Bridges?id=dRWnU6eLbYUC"]
]

Stephen_King_store = [[2155, "https://play.google.com/store/books/details/Stephen_King_From_a_Buick_8?id=4pbkeC8TTugC"]]

Patricia_Cornwell = [
    [2150, "https://play.google.com/store/books/details/Patricia_Cornwell_Body_of_Evidence?id=OgdXP7MxikwC"],
    [2351, "https://play.google.com/store/books/details/Patricia_Cornwell_All_That_Remains?id=rR3U1dINYY4C"],
    [3108, "https://play.google.com/store/books/details/Patricia_Cornwell_Cause_of_Death?id=EOaZ80nsXSIC"],
    [3680, "https://play.google.com/store/books/details/Patricia_Cornwell_Blow_Fly?id=SFlSRgO8WusC"],
    [4127, "https://play.google.com/store/books/details/Patricia_Cornwell_Black_Notice?id=-JgyuTpxO6wC"],
    [5007, "https://play.google.com/store/books/details/Patricia_Cornwell_Predator?id=dQZblzJcD5wC"],
    [5166, "https://play.google.com/store/books/details/Patricia_Cornwell_Scarpetta?id=PDd88wbLF-wC"],
    [5282, "https://play.google.com/store/books/details/Patricia_Cornwell_Book_of_the_Dead?id=tTu07zPQVTYC"],
    [6422, "https://play.google.com/store/books/details/Patricia_Cornwell_The_Scarpetta_Factor?id=-4JaSBhEmmgC"],
    [6878, "https://play.google.com/store/books/details/Patricia_Cornwell_The_Bone_Bed?id=xQFdRH1KXZMC"],
    [7268, "https://play.google.com/store/books/details/Patricia_Cornwell_Port_Mortuary?id=rsAC6aZSiV4C"]
]

'''

sub_books = pd.read_csv('../Data/sub_authors_us_50_100.csv')
sub_books = sub_books.drop(columns=['authors', 'original_title'])
id_to_urls = sub_books.values.tolist()

de = DataExtractor()
#de.extract_using_api('Stephen King', Stephen_King)
de.extract_from_url(id_to_urls)