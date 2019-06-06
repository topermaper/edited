# search.py

## Usage
python search.py --csv search_dataset.csv --qry query.txt --timeit True

This script loads both a csv file containing products and a query file to be run against.

-- def loadCSV --
This procedure loads the csv file into memmory and creates a 3-level index to speed up the search.
Index first level will be the first letter of the product, second level the whole word, third level will be the item position where it can be found and also will be stored the number of the token ocurrences so it can be used to create a search score.

-- def processQuery --
For each query token we have to check first whether it is in the index or not, first we will use the first character, and then if the whole word has the token as prefix we will use the index(self.itemIndex) to find the index for matching items.
Then if we have a match then we create a dictionary of matches containing the search score and a list of search tokens that did not match. When a query token matches it is removed from the list so the match can be discarded in case not all the query tokens matched.

-- def getScore --
I tried to keep the score function simple. It calculates how much of the word matched based on string lenght and is multiplied per number of ocurrences in the product.

Examples:
query "dress" matching "dress" scores 5/5 = 1
query "dress" matching "dressed" scores 5/7 because it partially matched. In case word dresses is found twice in the product description or brand then the score would be  5/7 x 2



Executing the script using the following query file took 15ms per query:
Green distres  man man man
yellow toywatch
asos skinny jeans
toyota car
floral dress b
red prada clutch
prada perforated runway duffel bag
guess top

topisimo@cheetah:~/edited$ python search.py --csv search_dataset.csv --qry query.txt --timeit True
1
2.075000,8524,Green distressed hibiscus print tankini top,Mantaray
1
2.000000,4838,Jelly Time Only watch yellow,Toywatch
9
4.000000,21883,ASOS PETITE Rich Indigo Skinny Jeans,Asos
4.000000,50698,ASOS PREMIUM Tuxedo Tab Skinny Jeans,Asos
4.000000,19579,ASOS Diamante Skinny Jeans,Asos
4.000000,41460,ASOS Side Zip Skinny Jeans,Asos
4.000000,50657,ASOS Skinny Carrot Jeans,Asos
4.000000,41401,ASOS CURVE Foil Armour Skinny Jeans,Asos
4.000000,40267,ASOS PETITE Silver Grey Skinny Jeans,Asos
4.000000,19584,ASOS Lace Up Skinny Jeans,Asos
4.000000,38097,ASOS Premium Washed Camo Skinny Jeans,Asos
0
106
2.916667,30222,Sleeveless Bold Floral Dress by Lane Bryant,Lanebryant
2.809524,212,Blurred Floral Sweetheart Dress by Lane Bryant,Lanebryant
2.750000,13865,Ellie Bow Back Floral Dress,Boohoo
2.750000,44454,Floral Tie Back Dress by Wal G**,Topshop
2.625000,46246,Silk floral polka dot dress,Boutique by Jaeger
2.533333,59645,Teens Tabitha Floral Printed Belted Brush Knit Dress,Boohoo
2.500000,19346,Folly Floral Ruffled Cover Up Dress,Marc by Marc Jacobs
2.500000,26722,Milly Viola Floral Printed Haley Dress,Milly by Michelle Smith
2.500000,3008,Fabulously Floral Turquoise Dress by Pink Apple,Lanebryant
2.500000,2561,Lace Floral Dress,See By Chloé
0
1
5.000000,44050,Perforated Runway Duffel Bag,Prada
17
3.833333,26015,GUESS Kids Girls' "Love Guess" Stripe Tank Top - Sizes S-XL,Guess
3.000000,57744,Guess Classic Top,Guess
3.000000,13107,Guess Logo Ribbed Vest Top,Guess
3.000000,31426,Guess Sequin Animal Tunic Top,Guess
2.000000,12623,GbyM Silk Top,Guess
2.000000,8957,Marilyn Corset Top,Guess
2.000000,30148,Lydia Print Top,Guess
2.000000,26418,Jilly Top Zip Crossbody,Guess
2.000000,11170,Ruffle Babydoll Top,Guess
2.000000,36544,Aviation Crossbody Top Zip,Guess

8 queries processed in 0.121573 seconds. 0.015197 seconds per query


# search_new.py

Speed improved version

## Usage

topisimo@cheetah:~/edited$ python search_new.py --csv search_dataset.csv --qry query.txt --timeit 2
1
2.075000,'8524','Green distressed hibiscus print tankini top','Mantaray'
1
2.000000,'4838','Jelly Time Only watch yellow','Toywatch'
9
4.000000,'21883','ASOS PETITE Rich Indigo Skinny Jeans','Asos'
4.000000,'50698','ASOS PREMIUM Tuxedo Tab Skinny Jeans','Asos'
4.000000,'19579','ASOS Diamante Skinny Jeans','Asos'
4.000000,'41460','ASOS Side Zip Skinny Jeans','Asos'
4.000000,'50657','ASOS Skinny Carrot Jeans','Asos'
4.000000,'41401','ASOS CURVE Foil Armour Skinny Jeans','Asos'
4.000000,'40267','ASOS PETITE Silver Grey Skinny Jeans','Asos'
4.000000,'19584','ASOS Lace Up Skinny Jeans','Asos'
4.000000,'38097','ASOS Premium Washed Camo Skinny Jeans','Asos'
0
106
2.916667,'30222','Sleeveless Bold Floral Dress by Lane Bryant','Lanebryant'
2.809524,'212','Blurred Floral Sweetheart Dress by Lane Bryant','Lanebryant'
2.750000,'13865','Ellie Bow Back Floral Dress','Boohoo'
2.750000,'44454','Floral Tie Back Dress by Wal G**','Topshop'
2.625000,'46246','Silk floral polka dot dress','Boutique by Jaeger'
2.533333,'59645','Teens Tabitha Floral Printed Belted Brush Knit Dress','Boohoo'
2.500000,'19346','Folly Floral Ruffled Cover Up Dress','Marc by Marc Jacobs'
2.500000,'26722','Milly Viola Floral Printed Haley Dress','Milly by Michelle Smith'
2.500000,'3008','Fabulously Floral Turquoise Dress by Pink Apple','Lanebryant'
2.500000,'2561','Lace Floral Dress','See By Chlo\xc3\xa9'
0
1
5.000000,'44050','Perforated Runway Duffel Bag','Prada'
17
3.833333,'26015','GUESS Kids Girls\' "Love Guess" Stripe Tank Top - Sizes S-XL','Guess'
3.000000,'57744','Guess Classic Top','Guess'
3.000000,'13107','Guess Logo Ribbed Vest Top','Guess'
3.000000,'31426','Guess Sequin Animal Tunic Top','Guess'
2.000000,'12623','GbyM Silk Top','Guess'
2.000000,'8957','Marilyn Corset Top','Guess'
2.000000,'30148','Lydia Print Top','Guess'
2.000000,'26418','Jilly Top Zip Crossbody','Guess'
2.000000,'11170','Ruffle Babydoll Top','Guess'
2.000000,'36544','Aviation Crossbody Top Zip','Guess'

8 queries processed in 0.060694 seconds. 0.007587 seconds per query
