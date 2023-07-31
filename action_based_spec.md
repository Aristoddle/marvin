# Marvin Platform - Action Based Specifications

This document provides an overview of the main components of the Marvin platform, their implementation, top-level use, and developer utility.

## AIModel

`AIModel` is a base class for AI models. It is used to extract structured data from text or generate structured data from text.

### Implementation

`AIModel` is implemented as a Pydantic `BaseModel` with additional methods for extracting and generating data.

### Top-Level Use

```python
from src.marvin.components.ai_model import AIModel

class Location(AIModel):
    city: str
    state: str
    latitude: float
    longitude: float

# Extract structured data from text
location = Location.extract("I live in San Francisco, California.")
print(location.city)  # "San Francisco"
print(location.state)  # "California"

# Generate structured data from text
location = Location.generate("I need a location in California.")
print(location.city)  # Some city in California
print(location.state)  # "California"
```

### Developer Utility

`AIModel` provides a way to leverage AI to parse natural language text into structured data or generate structured data from natural language text.

## ai_classifier

`ai_classifier` is a decorator that is used to transform a regular Enum class into an AIEnum class.

### Implementation

`ai_classifier` is implemented as a Python decorator that adds additional attributes and methods to an Enum class.

### Top-Level Use

```python
from src.marvin.components.ai_classifier import ai_classifier

@ai_classifier
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Classify text
color = Color("I like the color of the sky.")
print(color)  # Color.BLUE
```

### Developer Utility

`ai_classifier` provides a way to leverage AI to classify natural language text into predefined categories.

## AIApplication

`AIApplication` is a class that represents a stateful, autonomous, natural language interface to an application.

### Implementation

`AIApplication` is implemented as a Pydantic `BaseModel` with additional attributes and methods for maintaining state and interacting with the application.

### Top-Level Use

```python
from src.marvin.components.ai_application import AIApplication

class TodoApp(AIApplication):
    name = "Todo App"
    description = "A simple todo app."

# Create an instance of the app
app = TodoApp()

# Interact with the app
app("I need to go to the store.")
print(app.state)  # State of the app
print(app.plan)  # Plan of the app
```

### Developer Utility

`AIApplication` provides a way to create a natural language interface to an application that can maintain state and interact with the application autonomously.

## AIFunction

`AIFunction` is a class that represents a Python function with a signature and docstring as a prompt for an AI to predict the function's output.

### Implementation

`AIFunction` is implemented as a Pydantic `BaseModel` with additional methods for predicting function output.

### Top-Level Use

```python
from src.marvin.components.ai_function import ai_fn

@ai_fn
def add(a: int, b: int) -> int:
    """Adds two integers."""

# Predict function output
result = add(1, 2)
print(result)  # 3
```

### Developer Utility

`AIFunction` provides a way to leverage AI to predict the output of a Python function based on its signature and docstring.

## ScrapeGhost

ScrapeGhost is a tool for extracting structured data from web pages using GPT-3. It takes a schema that describes the shape of the data you wish to extract, and returns a dictionary of that shape.

### API Reference

#### `SchemaScraper`

The `SchemaScraper` class is the main interface to the API.

It has one required parameter:

* `schema` - A dictionary describing the shape of the data you wish to extract.

And the following optional parameters:

* `models` - *list\[str\]* - A list of models to use, in order of preference.  Defaults to `["gpt-3.5-turbo", "gpt-4"]`.  (See [supported models](../openai/#costs) for details.
* `model_params` - *dict* - A dictionary of parameters to pass to the underlying GPT model.  (See [OpenAI docs](https://platform.openai.com/docs/api-reference/create-completion) for details.)
* `max_cost` -  *float* (dollars) - The maximum total cost of calls made using this scraper. This is set to 1 ($1.00) by default to avoid large unexpected charges.
* `extra_instructions` - *list\[str\]* - Additional instructions to pass to the GPT model as a system prompt.
* `extra_preprocessors` - *list* - A list of preprocessors to run on the HTML before sending it to the API.  This is in addition to the default preprocessors.
* `postprocessors` - *list* - A list of postprocessors to run on the results before returning them.  If provided, this will override the default postprocessors.
* `auto_split_length` - *int* - If set, the scraper will split the page into multiple calls, each of this length. See auto-splitting for details.

#### `scrape`

The `scrape` method of a `SchemaScraper` is used to scrape a page.

```python
scraper = SchemaScraper(schema)
scraper.scrape("https://example.com")
```

* `url_or_html` - The first parameter should be a URL or HTML string to scrape.
* `extra_preprocessors` - A list of Preprocessors to run on the HTML before sending it to the API.

It is also possible to call the scraper directly, which is equivalent to calling `scrape`:

```python
scraper = SchemaScraper(schema)
scraper("https://example.com")
# same as writing
scraper.scrape("https://example.com")
```

#### Exceptions

The following exceptions can be raised by the scraper:

(all are subclasses of `ScrapeghostError`)

##### `MaxCostExceeded`

The maximum cost of the scraper has been exceeded.

Raise the `max_cost` parameter to allow more calls to be made.

##### `PreprocessorError`

A preprocessor encountered an error (such as returning an empty list of nodes).

##### `TooManyTokens`

Raised when the number of tokens being sent exceeds the maximum allowed.

This indicates that the HTML is too large to be processed by the API.

!!! tip

    Consider using the `css` or `xpath` selectors to reduce the number of tokens being sent, or use the `auto_split_length` parameter to split the request into multiple requests if necessary.

##### `BadStop`

Indicates that OpenAI ran out of space before the stop token was reached.

!!! tip

    OpenAI considers both the input and the response tokens when determining if the token limit has been exceeded.

    If you are using `auto_split_length`, consider decreasing the value to leave more space for responses.

##### `InvalidJSON`

Indicates that the JSON returned by the API is invalid.

### Usage

#### Data Flow

Since most of the work is done by the API, the job of a `SchemaScraper` is to make it easier to pass HTML and get valid output.

If you are going to go beyond the basics, it is important to understand the data flow:

1. The page HTML is passed through any [preprocessors](#preprocessors).

    a. The `CleanHTML` preprocessor removes unnecessary tags and attributes.  (This is done by default.)

    b. If an `XPath` or `CSS` preprocessor is used, the results are selected and re-combined into a single HTML string.

    c. Custom preprocessors can also execute here.

2. The HTML and schema are sent to the LLM with instructions to extract.

3. The results are passed through any [postprocessors](#postprocessors).

    a. The `JSONPostprocessor` converts the results to JSON.  (This is done by default.) If the results are not valid JSON, a second (much smaller) request can be made to ask it to fix the JSON.

    b. Custom postprocessors can also execute here.

You can modify nearly any part of the process to suit your needs.  (See [Customization](#customization) for more details.)

#### Auto-splitting

While the flow above covers most cases, there is one special case that is worth mentioning.

If you set the `auto_split_length` parameter to a positive integer, the HTML will be split into multiple requests where each
request aims to be no larger than `auto_split_length` tokens.

!!! warning

    In **list mode**, a single call can make many requests. Keep an eye on the `max_cost` parameter if you're using this.

    While this seems to work well enough for long lists of similar items, the question of it is worth the time and money is up to you.
    Writing a bit of code is probably the better option in most cases.

Instead of recombining the results of the `XPath` or `CSS` preprocessor, the results are instead chunked into smaller pieces (<= `auto_split_length`) and sent to the API separately.

The instructions are also modified slightly, indicating that your schema is for a list of similar items.

#### Customization

To make it easier to experiment with different approaches, it is possible to customize nearly every part of the process from how the HTML is retrieved to how the results are processed.

##### HTTP Requests

Instead of providing mechanisms to customize the HTTP request made by the library (e.g. to use caching, or make a `POST`), you can simply pass already retrieved HTML to the `scrape` method.

This means you can use any HTTP library you want to retrieve the HTML.

##### Preprocessors

Preprocessors allow you to modify the HTML before it is sent to the API.

Three preprocessors are provided:

* `CleanHTML` - Cleans the HTML using `lxml.html.clean.Cleaner`.
* `XPath` - Applies an XPath selector to the HTML.
* `CSS` - Applies a CSS selector to the HTML.

!!! note

    `CleanHTML` is always applied first, as it is part of the default preprocessors list.

You can add your own preprocessors by passing a list to the `extra_preprocessors` parameter of `SchemaScraper`.

```python
scraper = SchemaScraper(schema, extra_preprocessors=[CSS("table")])
```

It is also possible to pass preprocessors at scrape time:

```python
scraper = SchemaScraper(schema)
scraper.scrape("https://example.com", extra_preprocessors=[CSS("table")])
```

Implementing your own preprocessor is simple, just create a callable that takes a `lxml.html.HtmlElement` and returns a list of one or more `lxml.html.HtmlElement` objects.  Look at `preprocessors.py` for examples.

##### Altering the Instructions to GPT

Right now you can pass additional instructions to GPT by passing a list of strings to the `extra_instructions` parameter of `SchemaScraper`.

You can also pass `model_params` to pass additional arguments to the API.

```python
schema = {"name": "str", "committees": [], "bio": "str"}
scraper = SchemaScraper(
    schema,
    models=["gpt-4"],
    extra_instructions=["Put the legislator's bio in the 'bio' field. Summarize it so that it is no longer than 3 sentences."],
)
scraper.scrape("https://norton.house.gov/about/full-biography").data
```
```json
{'name': 'Representative Eleanor Holmes Norton',
 'committees': [
    'House Subcommittee on Highways and Transit',
    'Committee on Oversight and Reform',
    'Committee on Transportation and Infrastructure'
    ],
  'bio': 'Congresswoman Eleanor Holmes Norton has been serving as the congresswoman for the District of Columbia since 1991. She is the Chair of the House Subcommittee on Highways and Transit and serves on two committees: the Committee on Oversight and Reform and the Committee on Transportation and Infrastructure. Before her congressional service, President Jimmy Carter appointed her to serve as the first woman to chair the U.S. Equal Employment Opportunity Commission.'}
```

These instructions can be useful for refining the results, but they are not required.

##### Altering the API / Model

See <https://github.com/jamesturk/scrapeghost/issues/18>

#### Postprocessors

Postprocessors take the results of the API call and modify them before returning them to the user.

Three postprocessors are provided:

* `JSONPostprocessor` - Converts the results to JSON.
* `HallucinationChecker` - Checks the results for hallucinations.
* `PydanticPostprocessor` - Converts the results to JSON and validates them using a `pydantic` model.

By default, `JSONPostprocessor` and `HallucinationChecker` are enabled.

`HallucinationChecker` verifies that values in the response are present in the source HTML.  This is useful for ensuring that the results are not "hallucinations".
This is done as a proof of concept, and to help determine how big of an issue hallucinations are for this use case.

##### Using `pydantic` Models

If you want to validate that the returned data isn't just JSON, but data in the format you expect, you can use `pydantic` models.

```python
    from pydantic import BaseModel
    from scrapeghost import SchemaScraper, CSS


    class CrewMember(BaseModel):
        gender: str
        race: str
        alignment: str


    # passing a pydantic model to the SchemaScraper # will generate a schema from it
    # and add the PydanticPostprocessor to the postprocessors
    scrape_crewmember = SchemaScraper(schema=CrewMember)
    result = scrape_crewmember.scrape(
        "https://spaceghost.fandom.com/wiki/Zorak",
        extra_preprocessors=[CSS(".infobox")],
    )
    print(repr(result.data))
```

```log
    CrewMember(gender='Male', race='Dokarian', alignment='Evil\\nProtagonist')
```

This works by converting the `pydantic` model to a schema and registering a `PydanticPostprocessor` to validate the results automatically.

#### Pagination

One technique to handle pagination is provided by the `PaginatedSchemaScraper` class.

This class takes a schema that describes a single result, and wraps it in a schema that describes a list of results as well as an additional page.

For example:

```python
{"first_name": "str", "last_name": "str"}
```

Automatically becomes:

```python
{"next_page": "url", "results": [{"first_name": "str", "last_name": "str"}]}
```

The `PaginatedSchemaScraper` class then takes care of following the `next_page` link until there are no more pages.

!!! note

    Right now, given the library's stance on customizing requests being "just use your own HTTP library", the `PaginatedSchemaScraper` class does not provide a means to customize the HTTP request used to retrieve the next page.

    If you need a more complicated approach it is recommended you implement your own pagination logic for now,
    <https://github.com/jamesturk/scrapeghost/blob/main/src/scrapeghost/scrapers.py#L238> may be a good starting point.

    If you have strong opinions here, please open an issue to discuss.

It then takes the combined "results" and returns them to the user.

Here's a functional example that scrapes several pages of employees:

```python
    import json
    from scrapeghost.scrapers import PaginatedSchemaScraper


    schema = {"first_name": "str", "last_name": "str", "position": "str", "url": "url"}
    url = "https://scrapple.fly.dev/staff"

    scraper = PaginatedSchemaScraper(schema)
    resp = scraper.scrape(url)

    # the resulting response is a ScrapeResponse object just like any other
    # all the results are gathered in resp.data
    json.dump(resp.data, open("yoyodyne.json", "w"), indent=2)
```

!!! warning

    One caveat of the current approach: The `url` attribute on a `ScraperResult` from a `PaginatedSchemaScraper` is a semicolon-delimited list of all the URLs that were scraped to produce that result.



💬

# Duckduckgo_search<a name="TOP"></a>

Search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine. Downloading files and images to a local hard drive.

## Table of Contents
* [Install](#install)
* [CLI version](#cli-version)
* [Duckduckgo search operators](#duckduckgo-search-operators)
* [Regions](#regions)
* [Using proxy](#using-proxy)
* [1. text() - text search](#1-text---text-search-by-by-duckduckgocom)
* [2. answers() - instant answers](#2-answers---instant-answers-by-duckduckgocom)
* [3. images() - image search](#3-images---image-search-by-duckduckgocom)
* [4. videos() - video search](#4-videos---video-search-by-duckduckgocom)
* [5. news() - news search](#5-news---news-search-by-duckduckgocom)
* [6. maps() - map search](#6-maps---map-search-by-duckduckgocom)
* [7. translate() - translation](#7-translate---translation-by-duckduckgocom)
* [8. suggestions() - suggestions](#8-suggestions---suggestions-by-duckduckgocom)

## Install
```python
pip install -U duckduckgo_search
```

## CLI version

```python3
ddgs --help
```
or
```python3
python -m duckduckgo_search --help
```

CLI examples:
```python3
# text search
ddgs text -k 'ayrton senna'
# text search via proxy (example: Tor Browser)
ddgs text -k 'china is a global threat' -p socks5://localhost:9150
# find and download pdf files
ddgs text -k "russia filetype:pdf" -m 50 -d
# find in es-es region and download pdf files via proxy (example: Tor browser)
ddgs text -k "embajada a tamorlán filetype:pdf" -r es-es -m 50 -d -p socks5://localhost:9150
# find and download xls files from a specific site
ddgs text -k 'sanctions filetype:xls site:gov.ua' -m 50 -d
# find and download any doc(x) files from a specific site
ddgs text -k 'filetype:doc site:mos.ru' -m 50 -d
# find and download images
ddgs images -k "yuri kuklachev cat theatre" -m 500 -s off -d
# find in br-br region and download images via proxy (example: Tor browser) in 10 threads
ddgs images -k 'rio carnival' -r br-br -s off -m 500 -d -th 10 -p socks5://localhost:9150
# get latest news
ddgs news -k "ukraine war" -s off -t d -m 10
# get last day's news and save it to a csv file
ddgs news -k "hubble telescope" -t d -m 50 -o csv
# get answers and save to a json file
ddgs answers -k holocaust -o json
```
[Go To TOP](#TOP)

## Duckduckgo search operators

| Keywords example |	Result|
| ---     | ---   |
| cats dogs |	Results about cats or dogs |
| "cats and dogs" |	Results for exact term "cats and dogs". If no results are found, related results are shown. |
| cats -dogs |	Fewer dogs in results |
| cats +dogs |	More dogs in results |
| cats filetype:pdf |	PDFs about cats. Supported file types: pdf, doc(x), xls(x), ppt(x), html |
| dogs site:example.com  |	Pages about dogs from example.com |
| cats -site:example.com |	Pages about cats, excluding example.com |
| intitle:dogs |	Page title includes the word "dogs" |
| inurl:cats  |	Page url includes the word "cats" |

[Go To TOP](#TOP)

## Regions
<details>
  <summary>expand</summary>

    xa-ar for Arabia
    xa-en for Arabia (en)
    ar-es for Argentina
    au-en for Australia
    at-de for Austria
    be-fr for Belgium (fr)
    be-nl for Belgium (nl)
    br-pt for Brazil
    bg-bg for Bulgaria
    ca-en for Canada
    ca-fr for Canada (fr)
    ct-ca for Catalan
    cl-es for Chile
    cn-zh for China
    co-es for Colombia
    hr-hr for Croatia
    cz-cs for Czech Republic
    dk-da for Denmark
    ee-et for Estonia
    fi-fi for Finland
    fr-fr for France
    de-de for Germany
    gr-el for Greece
    hk-tzh for Hong Kong
    hu-hu for Hungary
    in-en for India
    id-id for Indonesia
    id-en for Indonesia (en)
    ie-en for Ireland
    il-he for Israel
    it-it for Italy
    jp-jp for Japan
    kr-kr for Korea
    lv-lv for Latvia
    lt-lt for Lithuania
    xl-es for Latin America
    my-ms for Malaysia
    my-en for Malaysia (en)
    mx-es for Mexico
    nl-nl for Netherlands
    nz-en for New Zealand
    no-no for Norway
    pe-es for Peru
    ph-en for Philippines
    ph-tl for Philippines (tl)
    pl-pl for Poland
    pt-pt for Portugal
    ro-ro for Romania
    ru-ru for Russia
    sg-en for Singapore
    sk-sk for Slovak Republic
    sl-sl for Slovenia
    za-en for South Africa
    es-es for Spain
    se-sv for Sweden
    ch-de for Switzerland (de)
    ch-fr for Switzerland (fr)
    ch-it for Switzerland (it)
    tw-tzh for Taiwan
    th-th for Thailand
    tr-tr for Turkey
    ua-uk for Ukraine
    uk-en for United Kingdom
    us-en for United States
    ue-es for United States (es)
    ve-es for Venezuela
    vn-vi for Vietnam
    wt-wt for No region
___
</details>

[Go To TOP](#TOP)

## Using proxy
*1. The easiest way. Launch the Tor Browser*
```python3
from duckduckgo_search import DDGS

with DDGS(proxies="socks5://localhost:9150", timeout=20) as ddgs:
    for r in ddgs.text("something you need"):
        print(r)
```
*2. Use any proxy server* (*example with [iproyal residential proxies](https://iproyal.com?r=residential_proxies)*)
```python3
from duckduckgo_search import DDGS

with DDGS(proxies="socks5://user:password@geo.iproyal.com:32325", timeout=20) as ddgs:
    for r in ddgs.text("something you need"):
        print(r)
```


## 1. text() - text search by duckduckgo.com
`html` and `lite` backend differ from `api`:</br>
* don't do an extra request first to get vqd,</br>
* use POST requests,</br>
* pause 0.75 seconds between paginations.</br>

If you use `html` or `lite` backend, pause at least 0.75 seconds between text() calls. 
Otherwise the site will return a 403 status code after a few requests and block your ip for a few seconds.
```python
def text(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    backend: str = "api",
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo text search generator. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        backend: api, html, lite. Defaults to api.
            api - collect data from https://duckduckgo.com,
            html - collect data from https://html.duckduckgo.com,
            lite - collect data from https://lite.duckduckgo.com.
    Yields:
        dict with search results.

    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.text('live free or die', region='wt-wt', safesearch='Off', timelimit='y'):
        print(r)

# Searching for pdf files
with DDGS() as ddgs:
    for r in ddgs.text('russia filetype:pdf', region='wt-wt', safesearch='Off', timelimit='y'):
        print(r)

# Using lite backend and limit the number of results to 10
from itertools import islice

with DDGS() as ddgs:
    ddgs_gen = ddgs.text("notes from a dead house", backend="lite")
    for r in islice(ddgs_gen, 10):
        print(r)
```


## 2. answers() - instant answers by duckduckgo.com

```python
def answers(keywords: str) -> Iterator[Dict[str, Optional[str]]]::
    """DuckDuckGo instant answers. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.

    Yields:
        dict with instant answers results.

        """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.answers("sun"):
        print(r)
```

## 3. images() - image search by duckduckgo.com

```python
def images(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    size: Optional[str] = None,
    color: Optional[str] = None,
    type_image: Optional[str] = None,
    layout: Optional[str] = None,
    license_image: Optional[str] = None,
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo images search. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: Day, Week, Month, Year. Defaults to None.
        size: Small, Medium, Large, Wallpaper. Defaults to None.
        color: color, Monochrome, Red, Orange, Yellow, Green, Blue,
            Purple, Pink, Brown, Black, Gray, Teal, White. Defaults to None.
        type_image: photo, clipart, gif, transparent, line.
            Defaults to None.
        layout: Square, Tall, Wide. Defaults to None.
        license_image: any (All Creative Commons), Public (PublicDomain),
            Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
            Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
            Use Commercially). Defaults to None.

    Yields:
        dict with image search results.

    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    keywords = 'butterfly'
    ddgs_images_gen = ddgs.images(
      keywords,
      region="wt-wt",
      safesearch="Off",
      size=None,
      color="Monochrome",
      type_image=None,
      layout=None,
      license_image=None,
    )
    for r in ddgs_images_gen:
        print(r)
```

## 4. videos() - video search by duckduckgo.com

```python
def videos(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
    resolution: Optional[str] = None,
    duration: Optional[str] = None,
    license_videos: Optional[str] = None,
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo videos search. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.
        resolution: high, standart. Defaults to None.
        duration: short, medium, long. Defaults to None.
        license_videos: creativeCommon, youtube. Defaults to None.

    Yields:
        dict with videos search results

    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    keywords = 'tesla'
    ddgs_videos_gen = ddgs.videos(
      keywords,
      region="wt-wt",
      safesearch="Off",
      timelimit="w",
      resolution="high",
      duration="medium",
    )
    for r in ddgs_videos_gen:
        print(r)
```

## 5. news() - news search by duckduckgo.com

```python
def news(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo news search. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.

    Yields:
        dict with news search results.

    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    keywords = 'How soon the sun will die'
    ddgs_news_gen = ddgs.news(
      keywords,
      region="wt-wt",
      safesearch="Off",
      timelimit="m",
    )
    for r in ddgs_news_gen:
        print(r)
```

## 6. maps() - map search by duckduckgo.com

```python
def maps(
        keywords,
        place: Optional[str] = None,
        street: Optional[str] = None,
        city: Optional[str] = None,
        county: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        postalcode: Optional[str] = None,
        latitude: Optional[str] = None,
        longitude: Optional[str] = None,
        radius: int = 0,
    ) -> Iterator[Dict[str, Optional[str]]]:
        """DuckDuckGo maps search. Query params: https://duckduckgo.com/params

        Args:
            keywords: keywords for query
            place: if set, the other parameters are not used. Defaults to None.
            street: house number/street. Defaults to None.
            city: city of search. Defaults to None.
            county: county of search. Defaults to None.
            state: state of search. Defaults to None.
            country: country of search. Defaults to None.
            postalcode: postalcode of search. Defaults to None.
            latitude: geographic coordinate (north–south position). Defaults to None.
            longitude: geographic coordinate (east–west position); if latitude and
                longitude are set, the other parameters are not used. Defaults to None.
            radius: expand the search square by the distance in kilometers. Defaults to 0.

        Yields:
            dict with maps search results

        """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.maps("school", place="Uganda"):
        print(r)
```


## 7. translate() - translation by duckduckgo.com

```python
def translate(
    self,
    keywords: str,
    from_: Optional[str] = None,
    to: str = "en",
) -> Optional[Dict[str, Optional[str]]]:
    """DuckDuckGo translate

    Args:
        keywords: string or a list of strings to translate
        from_: translate from (defaults automatically). Defaults to None.
        to: what language to translate. Defaults to "en".

    Returns:
        dict with translated keywords.
    """
```
***Example***
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    keywords = 'school'
    r = ddgs.translate(keywords, to="de")
    print(r)
```

## 8. suggestions() - suggestions by duckduckgo.com

```python
def suggestions(
    keywords,
    region: str = "wt-wt",
) -> Iterator[Dict[str, Optional[str]]]:
    """DuckDuckGo suggestions. Query params: https://duckduckgo.com/params

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".

    Yields:
        dict with suggestions results.
    """
```
***Example***
```python3
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.suggestions("fly"):
        print(r)
```


And, while we will be using the Marvin, ScrapeGhost, and GPT-4-32k APIs to power our webpage-processing system (unless the Scrapy crawler proves more effective), here is a simple example/run-through of the DuckDuckGo Search API you've provided:

```
1: Call DuckDuckGo
First, it calls duckduckgo to do a web search. Why duckduckgo? Because they are the easiest to use. No API key is required, just do the following:

from duckduckgo_search import ddg

...

query = "how to make a great pastrami sandwich"

results = ddg(query, max_results=10)
I’m using the python package duckduckgo_search.

Easy! The results are a list of dictionaries as follows:

[
  {
    "title": "How to Make a Classic Pastrami Sandwich - Pocket Change Gourmet",
    "href": "https://pocketchangegourmet.com/pastrami-sandwich/",
    "body": "Using a cutting board, slice up your tomatoes\u2014leaving enough thickness to give a nice height and flavor to the finished sandwich. If you need to prepare your lettuce, this is also the best time to get on that. Dont forget to go back over and stir the onions on occasion to prevent uneven cooking. 2. The Bread."
  },
  {
    "title": "Ultimate Pastrami Sandwiches Recipe: How to Make It - Taste of Home",
    "href": "https://www.tasteofhome.com/recipes/ultimate-pastrami-sandwiches/",
    "body": "Drain cabbage. In a small bowl, combine the salt, celery seed, pepper and remaining sugar and vinegar; pour over cabbage and toss to coat. On an ungreased baking sheet, divide pastrami into 4 stacks; top each with cheese. Bake at 450\u00b0 for 2-3 minutes or until cheese is melted. Place pastrami on 4 toast slices."
  }
]
I’m currently ignoring everything except the urls, like this:

    urls = [result['href'] for result in results]
    urls = urls[:numresults] # just in case
2: Use the Scrapy webspider to download all the pages
Scrapy is a serious application for spidering through websites.

Scrapy is available via the python package scrapy.

It’s intended to be used directly on the cli, but you can actually use it inside your python scripts:

That’s how I’m using it.

To make use of Scrapy, I need to create a scrapy.Spider subclass:

import scrapy

class MySpider(scrapy.Spider):
    '''
    This is the spider that will be used to crawl the webpages. 
    We give this to the scrapy crawler.
    '''
    name = 'myspider'
    start_urls = None
    clean_with_llm = False 
    results = []

    def __init__(self, start_urls, clean_with_llm, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.clean_with_llm = clean_with_llm

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
      # In here, response contains the downloaded web page. 
      # I'll get to what to actually do with it below
      ...
It’s pretty simple: I give it a list of urls to visit, and the clean_with_llm setting. In start_requests, I yield each url, which tells Scrapy to go fetch them. In parse, scrapy is giving me one of the web pages, and I can process it.

Note: We could use selenium, or even better playwright, to do a better job of fetching the page, where it would run client side javascript first. I’ve not done this in this article, but note that it is possible.

Now that we’ve got the spider class, how do we invoke scrapy? Like this:

from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(MySpider, urls, clean_with_llm)
process.start()

# here the spider has finished downloading the pages and cleaning them up
return MySpider.results
There are apparently a whole ton of settings you can use for scrapy, I’ve just used it with all defaults. Seems to work, but it’s worth investigating them for more complex tasks.

Note: I do all kinds of hackery to control logging in ddgsearch, and I’ve left that out of this article. Getting scrapy to do its job without barfing into stdout isn’t simple, have a look at my code to behold my mad hacks.

So the final result from the function is in MySpider.results. But how does that get set? It gets set when we…

3. Use the parse method to clean up and return the results
Here’s my parse method:

def parse(self, response):
    body_html = response.body.decode('utf-8')

    url = response.url

    soup = bs4.BeautifulSoup(body_html, 'html.parser')
    title = soup.title.string
    text = soup.get_text()
    text = remove_duplicate_empty_lines(text) 

    if self.clean_with_llm:
        useful_text = extract_useful_information(url, title, text, 50)
    else:
        useful_text = readability(body_html)
    useful_text = remove_duplicate_empty_lines(useful_text)

    self.results.append({
        'url': url,
        'title': title,
        'text': text,
        'useful_text': useful_text
    })
What’s this doing?

First, it gets the body from the response. That’s the actual web page’s html.

hmm, looking at that, maybe I need to check the status code before proceeding? My experience is that scrapy doesn’t call parse unless the response is a 200.

Now, I need to return url, title, text, and useful_text.

url comes from response, easy.

I use BeautifulSoup to parse the web page, and get the title and the text. Also fairly easy.

Unfortunately, text can be long and full of garbage. I just want the useful bits that are about what the search is about. 

[continued by author, but not relevant to us]
```