from typing import Literal

SoilPh = Literal['Acid', 'Neutral', 'Alkaline']
SoilType = Literal['Clay', 'Sand', 'Chalk', 'Loam']
SoilMoisture = Literal['Moist but well-drained', 'Poorly-drained', 'Well-drained']
Duration = Literal['Annual', 'Biennial', 'Perennial']
PlantParts = Literal['Bark', 'Fruit', 'Flower', 'Habit', 'Leaf', 'Other', 'Root', 'Stem', 'Seed', 'Tuber', 'Foliage']
PositionSunlight = Literal['Partial shade', 'Full sun', 'Full shade']
PositionSide = Literal['East-facing', 'North-facing', 'West-facing', 'South-facing']
Seasons = Literal['Spring', 'Summer', 'Autumn', 'Winter']
ToxicTypes = Literal[
    'Toxic to Cats',
    'Slightly Toxic to Humans',
    'Moderate Toxic to Humans',
    'Highly Toxic to Humans',
    'Toxic to Dogs',
]
FoliageTypes = Literal['Deciduous', 'Evergreen', 'Semi evergreen']
HabitTypes = Literal[
    'Tufted',
    'Trailing',
    'Pendulous weeping',
    'Clump forming',
    'Columnar upright',
    'Submerged',
    'Suckering',
    'Floating',
    'Matforming',
    'Bushy',
    'Climbing',
]
Exposure = Literal['Exposed', 'Sheltered', 'Exposed or Sheltered', 'Sheltered or Exposed']
SeasonsMax = Literal[
    'Winter',
    'Spring',
    'Mid autumn',
    'Mid summer',
    'Summer',
    'Autumn',
    'Late autumn',
    'All year around',
    'Mid spring',
    'Mid winter',
    'Late summer',
    'Early autumn',
    'Late winter',
    'Early summer',
    'Late spring',
    'Early spring',
    'Early winter',
]
DistributionsTypes = Literal[
    'Native',
    'Introduced',
    'Doubtful',
    'Absent',
    'Extinct',
]
