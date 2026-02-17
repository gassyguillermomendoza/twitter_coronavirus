for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
  nohup python3 map.py --input_path "$file" --output_folder /home/gmendoza/bigdata/twitter_coronavirus/src/mapper_results &
done
