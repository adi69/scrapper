
backup_dir=results

today=$(date +"%d-%m-%y")
output_dir=$backup_dir/$today
mkdir $output_dir

products=('Delhi-Noida'
'Gurgaon'
'Kolkata'
'Mumbai'
'Pune'
'Ahmedabad-Gandhinagar'
'Bangalore'
'Hyderabad'
'Chennai'
)

index=0
for item in ${products[@]}
do
    title=BB_$item\_$today
    csvfile=$output_dir/$title.csv
    scrapy crawl bbspider -o $csvfile -a city=$item
    body='PFA.  --  Best, Tech Team'
    echo $body | mail -s $title -A $csvfile -t shaurya.shukla@grofers.com aditya.bhardwaj@grofers.com
    index=$((index+1))
done
