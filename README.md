# league-of-legends-replay-extractor
League of Legends Replay Extractor Using CV

A program for gathering positional data and providing analytics from League of Legends videos. It can be used to automatically gather spatiotemporal data (player locations over time) from a series of Youtube/locally stored videos

![image](https://github.com/kimsy1106/league-of-legends-replay-extractor/assets/53938323/2f030a34-542f-4da6-a915-ac8f65b514be)

For more information, see the wiki

#### 1. Download or clone the repo

Download directly from github and unzip or clone from the command line

#### 2. Install Requirements

    pip install -r requirements.txt

#### 3. How to Use

  - Collecting Player MatchIDs  :
    
        python3 generator.py
  - Replay File(.rofl) Download :

        python3 downloader.py
  - Replay Running & Recording  :

        python3 scraper.py

#### 4. Get Minimap Capture Images

![82_minimap](https://github.com/kimsy1106/league-of-legends-replay-extractor/assets/53938323/25838fe3-e9c0-4823-b5cd-40e0713d6364)


#### 5. You can make them( Using Minimap Frame dataset )

- Champion Tracking (Roboflow)
![image](https://github.com/kimsy1106/league-of-legends-replay-extractor/assets/53938323/fc383c7a-bdac-4c9e-b6e0-fad2bb639aa7)

Then, You can use this tracking model ( Performance | mAP : 92.2% | precision : 91.3% | recall : 90.2% )
- Infer on Local and Hosted Images
    To install dependencies,

        pip install roboflow.

    Then, add the following the following code snippet to a Python script:
  
        from roboflow import Roboflow
        rf = Roboflow(api_key="API_KEY")
        project = rf.workspace().project("lolpago-multi-tracking-service")
        model = project.version(18).model
        
        # infer on a local image
        print(model.predict("your_image.jpg", confidence=40, overlap=30).json())
        
        # visualize your prediction
        # model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")
        
        # infer on an image hosted elsewhere
        # print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())

