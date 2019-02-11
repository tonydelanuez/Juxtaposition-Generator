# Juxtaposition Generator

Web application written in Python and JavaScript that generates combinations of comments from an adult video website and inspirational wallpapers from reddit.com. 

## Disclaimer

Any content generated from this application is not own, and is likely highly offensive. The comments and images rendered from scraping comment data do not represent my own opinions nor those of my employer. 

**By viewing this source you agree that you are 18+ years of age or are of legal viewing age for adult content in your country.**


## Examples

Some very tame examples of the output:

![I could watch this all day](example_1.png?raw=true "I could watch this all day")

![Wow beautiful](example_2.png?raw=true "wow beautiful")


## Installation

Download the package as a zip or clone, then install the requirements. 

* `pip install -r requirements.txt`

## Usage

Once all the dependencies are installed run in another terminal:

* `sudo mongod` 

This starts the mongoDB server. 

Finally, start the app with: 

* `python app.py`

Then point your browser to [localhost port 5000](http://localhost:5000) and the app should be working. Initial startup is slow due to the python web scraping. 


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits

Made by me, [Tony De La Nuez](http://tonydelanuez.com) during a weekend where I clearly had too much free time. 

## License

MIT
