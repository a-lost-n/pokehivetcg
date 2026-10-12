clean:
	rm -f image_cropper/report/*.png; rm -f image_cropper/uncropped_report/*.png

clean-datasets:
	rm -f archetype_encoder/datasets/*.xlsx
	rm -f archetype_encoder/merged_datasets/*.xlsx

major-report:
	python3 archetype_encoder/main.py