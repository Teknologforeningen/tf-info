# TF - Info

A static site to be displayed on info-screens around [Teknologföreningen](https://www.teknologforeningen.fi). The site
is build entirely with [Deno](https://deno.land). Deno's standard library is utilized as much as possible.

## Installation

### Requirements

- [Deno](https://deno.land)

### Environmental variables

See `.env.example`

## Running

### Development

The development server can be run with the following command:

`deno task dev`

### Scripts

To also run scripts locally (for refreshing the page, changing languages and working clock):

`deno task scripts` 

## htmx

[htmx](https://htmx.org/) is used to solve some common problems. However, the machine running the website is running a
very old version of Google Chrome. Due to this some polyfills are needed. Additionally, htmx had to be modified
slightly; the reason to it being included in this repository.
