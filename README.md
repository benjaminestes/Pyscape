# Pyscape

A script to grab data from the [Mozscape API](http://apiwiki.seomoz.org/). Uses Python 3.

## Getting started

To use Pyscape you will need:

1. A Python 3 installation.
2. A set of [Mozscape API credentials](http://apiwiki.seomoz.org/create-and-manage-your-account), free or paid.

[NBED instructions]

### Examples

## Available API calls

### `links`

### `url-metrics`

### `anchor`

## OSE reports

Often use of the Mozscape API is an extension of working with [Open Site Explorer](http://www.opensiteexplorer.org/). When then 10,000 lines it provides are insufficient, we can use the command line to extend the amount of information available. Or, if we're just trying to pull a lot of reports it will be more convenient to use a command line tool.

I any case, given a URL the included ose.py uses the a Pyscape object to get the requisite data and formats it to match OSE output. Output filenames are determined by the input URL.

```bash
ose.py [URL] [OUTPUT]
```

## Using free API credentials

[NBED]

## Thanks

The [SEOmoz team](http://www.seomoz.org/about/team) deserves a lot of credit for their work on creating a useful tool. If you're a dev looking for a great place to work, [check them out](http://www.seomoz.org/about/jobs). And tell them I sent you!
