
backup_dir=results

today=$(date +"%d-%m-%y")
output_dir=$backup_dir/$today
mkdir $output_dir

products=('AC'
'WashingMachine'
'Cooler'
)

urls=('http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cabm%2Cc54&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cabm%2C8qx&pincode=122001&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drecency_desc&sid=j9e%2Cabm%2C52j&pincode=122001&filterNone=true&start='
)

#'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=tyy%2C4io&filterNone=true&start='

index=0
for item in ${products[@]}
do
    title=FK_$item\_data_$today
    csvfile=$output_dir/$title.csv
    scrapy crawl FkProduct -o $csvfile -a url_pattern=${urls[$index]}
    body='PFA.  --  Best, Tech Team'
    echo $body | mail -s $title -A $csvfile -t prateek@grofers.com aditya.bhardwaj@grofers.com
    index=$((index+1))
done
