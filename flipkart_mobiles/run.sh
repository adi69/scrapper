
backup_dir=results

today=$(date +"%d-%m-%y")
output_dir=$backup_dir/$today
mkdir $output_dir

products=('Mobile'
'AC'
'WashingMachine'
'Cooler'
'BluetoothSpeaker'
'Earphones'
'WaterPurifier'
'InductionCooktop'
'MixerJuicerGrinder'
'AirPurifier'
'Iron'
'MicrowaveOven'
'TV'
'Refrigerator'
)

urls=('http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=tyy%2C4io&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cabm%2Cc54&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cabm%2C8qx&pincode=122001&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Drecency_desc&sid=j9e%2Cabm%2C52j&pincode=122001&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=facets.wired%252Fwireless%255B%255D%3DWired%2B%2526%2BWireless&p%5B%5D=facets.wired%252Fwireless%255B%255D%3DWireless&sid=tyy%2C4mr%2C5ev&pincode=560068&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=search.flipkart.com&filterNone=true&q=earphones&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cabm%2Ci45&pincode=560068&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cm38%2C575&pincode=122001&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cm38%2C7ek&pincode=122001&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cabm%2C3o4&pincode=122001&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cabm%2Ca0u&pincode=122001&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=sort%3Dprice_asc&sid=j9e%2Cm38%2Co49&pincode=122001&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=ckf%2Cczl&pincode=122001&filterNone=true&start='
'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=j9e%2Cabm%2Chzg&pincode=122001&filterNone=true&start='
)

index=0
for item in ${products[@]}
do
    title=FK_$item\_data_$today
    csvfile=$output_dir/$title.csv
    scrapy crawl FkProduct -o $csvfile -a url_pattern=${urls[$index]}
    body='PFA.  --  Best, Tech Team'
    echo $body | mail -s $title -A $csvfile -t electronics@grofers.com aditya.bhardwaj@grofers.com
    index=$((index+1))
done

