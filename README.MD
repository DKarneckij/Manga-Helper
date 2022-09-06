## Intro

Manga-Helper is a personal web-scraping Discord Bot that helps me find cheap prices for out of print manga volumes that I would like to collect. In a Google Sheet worksheet I have a large list of links to volumes on a particular website. The bot’s main function is to retrieve the price of the item if it’s in stock, as well as the price of it on a website called AbeBooks that I use as a reference to decide whether the price is worth it.

## Commands
 
$sr
- Runs a single search for prices

$pr
- Sends the previous search result as an embed. Needed as the buttons used to navigate the pages stop working after some time has passed

$pr m
- Same as $pr but formatted better for mobile use

$remove 
- Removes listed volumes from the original list, and from the stored previous run

## Example

<img src="https://i.imgur.com/iy9otE1.png" alt="drawing" width="370"/>

## Roadmap

- [x] Add command to view previous search
- [x] Loop search every hour
- [x] Show new items compared to previous search
- [x] Add command to remove items from the listx
- [ ] Clean code 
