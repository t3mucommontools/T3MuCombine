cp datacards/$1/*txt datacards
cp workspaces/$1/*.root workspaces
cd datacards;

echo "==================================="
echo "            Combined               "
echo "==================================="
./runLimit.py -i CMS_T3MSignal_13TeV_Combined.txt

for cat in A B C; do
   for sub in 1 2; do
      echo "==================================="
      echo "               ${cat}${sub}                  "
      echo "==================================="
      ./runLimit.py -i CMS_T3MSignal_13TeV_${cat}${sub}.txt
   done
done

cd -
rm workspaces/*root datacards/*txt datacards/*root
