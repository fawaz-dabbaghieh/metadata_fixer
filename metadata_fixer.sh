#!/bin/bash

printf "This Script should \"Theoretically\" solve most of the metadata problems\n\n"

printf "Before procedding, this script only workes if you have unzipped the other scripts (Python, R, Sh) all in the same directory \n\n"

printf "Also make sure that your metadata file is named \"metadata\" and has two directories (experiment, sample)\n\n"

printf "If you're sure you want to proceed, then type (y) if you want to exit type (n)\n\n"

read answer

if [[ "$answer" == "y" || "Y" ]]; then

#maing code

WORKING_DIR=$(pwd)

mkdir tmp_metadata
cp -a metadata*/* tmp_metadata/

ls tmp_metadata/experiment/ > tmp_metadata/experiment/exp_dir.txt && sed '/exp_dir.txt/d' tmp_metadata/experiment/exp_dir.txt > tmp_metadata/experiment/tmp && mv tmp_metadata/experiment/tmp tmp_metadata/experiment/exp_dir.txt

mkdir tmp_metadata/experiment/all_experiments
cp -rf tmp_metadata/experiment/*/* tmp_metadata/experiment/all_experiments

cd tmp_metadata/experiment/all_experiments

find ./ -name "*emd.csv" | xargs -I '{}' basename '{}' | sed 's/\.csv//' | xargs -I '{}' mv '{}.csv' '{}.tsv'
find ./ -name "*emd.txt" | xargs -I '{}' basename '{}' | sed 's/\.txt//' | xargs -I '{}' mv '{}.txt' '{}.tsv'

cd ../../../
#fixing up the documents before using python
ls tmp_metadata/experiment/all_experiments/ > tmp_metadata/experiment/all_experiments/experiments.txt && sed '/experiments.txt/d' tmp_metadata/experiment/all_experiments/experiments.txt > tmp_metadata/experiment/all_experiments/tmp && mv tmp_metadata/experiment/all_experiments/tmp tmp_metadata/experiment/all_experiments/experiments.txt

#removing the space in keys and removing empty lines
echo "Wait for it"
for f in tmp_metadata/experiment/all_experiments/*emd.tsv
do
	#removing space from the key value
	sed -i 's/RNA ADAPTER/RNA_ADAPTER/g' $f
	
	#removing empty lines with any white space
	sed '/^\s*$/d' $f > tmp_metadata/experiment/all_experiments/tmp && mv tmp_metadata/experiment/all_experiments/tmp $f

done

#checking encoding
echo "Wait for it"
for f in tmp_metadata/experiment/all_experiments/*emd.tsv
do
	file $f
done > tmp_metadata/experiment/all_experiments/encoding.txt

grep ISO tmp_metadata/experiment/all_experiments/encoding.txt | awk -F ":" '{print $1}' > tmp_metadata/experiment/all_experiments/iso_files.txt

#converting encoding
echo "Wait for it"
while read f
do
	iconv -f ISO-8859-1 -t UTF-8//TRANSLIT $f > tmp_metadata/experiment/all_experiments/tmp && mv tmp_metadata/experiment/all_experiments/tmp $f

done < tmp_metadata/experiment/all_experiments/iso_files.txt

#removing the encoding problem character
echo "Wait for it"
for f in tmp_metadata/experiment/all_experiments/*emd.tsv
do
sed 's/Â//g' $f > tmp_metadata/experiment/all_experiments/tmp && mv tmp_metadata/experiment/all_experiments/tmp $f

done

ls tmp_metadata/experiment/all_experiments/*emd.tsv | awk -F "/" '{print $4}' > tmp_metadata/experiment/all_experiments/files.txt

cp files_fixer.py tmp_metadata/experiment/all_experiments/
#cp exp_tables.R tmp_metadata/experiment/all_experiments/
cd tmp_metadata/experiment/all_experiments/
mkdir after_python
python files_fixer.py

mkdir keys
cd after_python/
for f in *emd.tsv; do cat $f | awk -F "\t" '{print $1}' > ../keys/$f; done
 
#cp exp_tables.R after_python/

cp ../../../../exp_tables.R exp_tables.R
Rscript exp_tables.R
cd ../../../../


			##Now Samples###


for f in tmp_metadata/sample/*smd.txt
do

	#removing empty lines with any white space
	sed '/^\s*$/d' $f > tmp_metadata/sample/tmp && mv tmp_metadata/sample/tmp $f

done

#checking encoding
echo "Wait for it"
for f in tmp_metadata/sample/*smd.txt
do
	file $f
done > tmp_metadata/sample/encoding.txt

grep 'UTF-16' tmp_metadata/sample/encoding.txt | awk -F ":" '{print $1}' > tmp_metadata/sample/utf16_files.txt


#converting encoding
echo "Wait for it"
while read f
do
	iconv -f UTF-16 -t UTF-8//TRANSLIT $f > tmp_metadata/sample/tmp && mv tmp_metadata/sample/tmp $f

done < tmp_metadata/sample/utf16_files.txt

#removing the encoding problem character
echo "Wait for it"
for f in tmp_metadata/sample/*smd.txt
do
sed 's/Â//g' $f > tmp_metadata/sample/tmp && mv tmp_metadata/sample/tmp $f

done

##here comes python
ls tmp_metadata/sample/*smd.txt | awk -F "/" '{print $3}' > tmp_metadata/sample/files.txt

cp files_fixer.py tmp_metadata/sample/
cp sample_tables.R tmp_metadata/sample/
cd tmp_metadata/sample/
mkdir after_python
python files_fixer.py

mkdir keys
cd after_python/
for f in *smd.txt; do cat $f | awk -F "\t" '{print $1}' > ../keys/$f; done
cp ../../../sample_tables.R sample_tables.R
Rscript sample_tables.R
cd ../../../

		######running open refine and refining the tables######
mkdir final_tables
cp tmp_metadata/sample/after_python/all_samples.tsv final_tables/
cp tmp_metadata/experiment/all_experiments/after_python/all_experiments.tsv final_tables/

cp -t final_tables/ refine_exp.py refine.py refine_samples.py operations.json

bash openrefine-2.7-rc.1/refine &

sleep 7

cd final_tables/
mkdir filtered_exp
mkdir filtered_samples
python ../refine_exp.py > all_experiments_after_json.tsv
python ../refine_samples.py > all_samples_after_json.tsv

sed '/^\s*$/d' all_experiments_after_json.tsv > tmp && mv tmp all_experiments_after_json.tsv
sed '/^\s*$/d' all_samples_after_json.tsv > tmp && mv tmp all_samples_after_json.tsv

python ../all_exp_to_tsv.py
python ../all_samples_to_tsv.py

for f in *emd.tsv; do sed '/^\s*$/d' $f > tmp && mv tmp $f; done
for f in *smd.txt; do sed '/^\s*$/d' $f > tmp && mv tmp $f; done

		
		#####filtering the files against there keys#####
cp ../*filterin* ../final_tables/
ls *smd.txt > sample.txt
ls *emd.tsv > exp.txt
python samples_key_filtering.py
python exp_key_filtering.py
cd ../
		#####making final metadata#####

mkdir metadata_fixed
mkdir metadata_fixed/sample
mkdir metadata_fixed/experiment
mv final_tables/filtered_samples/*smd.txt metadata_fixed/sample/

while read f
do
	mkdir metadata_fixed/experiment/$f
done < tmp_metadata/experiment/exp_dir.txt

while read f
do
	mv final_tables/filtered_exp/$f* metadata_fixed/experiment/$f/

done < tmp_metadata/experiment/exp_dir.txt

#rm -r final_tables
rm -r tmp_metadata


else
	printf "your input was invalid, please run again and chose (y) if you want to continue\n"
	exit 1
fi

