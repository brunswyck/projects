# Data preprocessing - NYC Motor Vehicle Crashes

- Repository: `nyc-crashes`
- Type of Challenge: `Consolidation`
- Duration: `2 days`
- Deadline: `dd/mm/yy H:i AM/PM`
- Deployment strategy :
  - GitHub page
- Team challenge : `solo`

![NYC Picture (Image)](https://images.nycgo.com/image/fetch/q_70,w_900/https://www.nycgo.com/images/uploads/NY_in_3_days/TimeSquare-Manhattan-NYC-BrittanyPetronella_0069sat.jpg)

## Mission objectives

- Be able to use pandas
- Be able to clean a data set
- Be able to do prepare a data set for a machine learning model

## The Mission

Bill de Blasio, mayor of New York City, is in a bit of a pickle. Indeed, his police department, the NYPD, collected information about all the traffic accidents that happened in New York City. However, they are too busy eating doughnuts to correctly encode each traffic incident, and so it happens that the dataset that we got here is quite dirty, has a lot of missing values and can't be used by a machine learning model as is.
Can you help Mr. de Blasio and shine a new light on his police department ?

What he wants exactly is to predict which streets are the most dangerous while visiting the [city that never sleeps](https://en.wikipedia.org/wiki/The_City_That_Never_Sleeps).

I am sure that you are well-equipped to handle this.

### Must-have features

- The dataset contains no missing values ("" or null)
- No duplicates.
- Values are consolidated
- Data format is correct
- No blank spaces (ex: `" I love python "` => `"I love python"`)

### Nice-to-have features

- The more rows of data you use, the better. However, pay attention that the more data you have, the longer each operation needs to execute.
- Add new features computed using the features present that you think are going to be useful.
- Apply the preprocessing steps needed so that a future machine learning model can make the best use out of it **(feature selection, feature engineering, feature normalization, and resampling)**

### Miscellaneous information

An example dataset `data_100000.csv` has already been downloaded for you in
[../../additional_resources/datasets/NYC Motor Vehicle Crashes/](../../additional_resources/datasets/NYC%20Motor%20Vehicle%20Crashes/data_100000.csv), which has 100000 rows for around 21.5 MB. The full file is more than 10x larger, but it is not required to use the full file. However, **please use at least 100 000 rows** for the final version. Of course, you can always test your code on smaller data sets.

If you want to download a differently sized dataset, you can use the script `download.py` located in
[../../additional_resources/datasets/NYC Motor Vehicle Crashes/](../../additional_resources/datasets/NYC%20Motor%20Vehicle%20Crashes/download.py)
It will create a CSV file similar to `data_100000.csv` in your current directory.

See the usage of the script using

```bash
python download.py -h
```

You will need the `sodapy` library for downloading the data set.

```bash
pip install sodapy
```

## Deliverables

1. Publish your source code on the GitHub repository.
2. Create final `.csv` file with the cleaned dataset
3. Pimp up the README file:
   - Description
   - Installation
   - Usage
   - (Visuals)
   - (Contributors)
   - (Timeline)
   - (Personal situation)

### Steps

1. Create the repository
2. Study the request (What & Why ?)
3. Identify technical challenges (How ?)

Import the data set using

```python
import pandas as pd
df = pd.read_csv('data_100000.csv')
```

It is always hard to start a project, there are a million things to check.
Here are a few that might be needed in this data set.

Bill de Blasio wants to know and predict the dangerousness of the streets in New York.

- Ask yourself what your target variable will be.

  - Deaths/injuries/both ?
  - How about passengers/driver/pedestrians/cyclists ?

- Can values be consolidated? (e.g. `Truck` and `truck` refer to the same thing)
- Are there some columns where most of the data is missing ?
- Can you fill in some missing values ?
- Is the date format correct?
- Are some values integers that should be float or vice-versa ? Change the `dtype`.

During the cleaning process, you might ask yourself some questions like:

- _When should I drop my column when I have missing data ?_
- _What do I do if I can't fill in every missing value ?_
- _How long should my cleaning process take to run ?_

And the response is: **it depends.**
Indeed, it depends on the precision that you need.

If Bill de Blasio just wants a quick and dirty version, and you only have 2 days, well, have a quick dirty version ready as quick as possible.
Bill de Blasio gives you 2 weeks to have a very precise dataset ? Well, you can invest more time into getting every last bit of data cleaned.

One advice: **Start small, then be more precise if you have more time.**
You can have multiple final cleaned datasets, like:

1. `data_clean_GOOD_ENOUGH.csv`
2. `data_clean_GOOD.csv`
3. `data_clean_PRECISE.csv`

## Evaluation criteria

| Criteria       | Indicator                                                                      | Yes/No |
| -------------- | ------------------------------------------------------------------------------ | ------ |
| 1. Is complete | The student has realized all must-have features.                               |        |
|                | There is a published GitHub page available.                                    |        |
| 2. Is Correct  | There are no warnings or errors when running the script.                       |        |
|                | The final `.csv` file can be opened and is in a clean state.                   |        |
|                | The learner has used functions and minimized code duplication.                 |        |
|                | The learner can explain why and how he replaced missing values.                |        |
| 3. Is great    | Significantly more than 100000 rows have been used.                            |        |
|                | Features were normalized and categorical variables have been encoded properly. |        |

## A final note of encouragement

You've been waiting for this, and I'm certain that you are ready for it.

![You've got this!](https://media.giphy.com/media/ctNDDU3a4ffK1su6yJ/giphy.gif)
