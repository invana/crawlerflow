# InvanaBot

A spider cum data aggregation framework that can transform Websites, Feeds, APIs into Datasets with Crawl,
Transform and Index strategy; with configurations instead of code.
 
The framework comes with standard extractors that comes handy for most of the usecases. And gives you a way to 
write your own extraction strategy. The framework comes with integrations to [MongoDB](https://www.mongodb.com/)
 and [Elasticsearch](https://www.elastic.co/products/elasticsearch) by default, 
allowing you to save your data into your preferred database.

Some reasons you might want to use InvanaBot:

- No or least coding experience need, depending on the depth of your use-case.
- You can crawl a single site or traverse between multiple sites with just configuration.
- Data Storages like MongoDB and Elasticsearch are integrated already for use, Many more to join
- Built on top of Scrapy, so the core engine is Battle tested.

## Architecture

InvanaBot strategy relies on Crawl + Transform + Index Strategy, allowing user to traverse between 
multiple domains using just configuration..


## Requirements

Built with Python 3.6.x, **So python 2.7.x is not supported**. While the support might expand to
 more versions of Python 3x in near future. We are not planning on supporting 2.7 
 as it is reaching its end of life soon.
 

## Installation

Install using pip...

```bash
pip install invana-bot
```

...or clone the project from github.

```bash
pip install git+https://github.com/invanalabs/invana-bot#egg=invana_bot
```

## Quickstart

Can't wait to get started? The [quickstart](tutorials/quickstart.md) guide is the fastest way to setup a spider up and running.
 
 
## Support

For priority support please sign up for a professional or premium sponsorship plan. Get in touch with us 
at [sales@invanalabs.ai](emailto:sales@invanalabs.ai)

For updates on InvanaBot, you may also want to follow the [#InvanaBot](https://twitter.com/hashtag/InvanaBot?lang=en)
 or [@InvanaLabs](https://twitter.com/invanalabs) on Twitter.


## License


Copyright © 2016-present, Invana Technology Solutions Pvt Ltd. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.

Neither the name of the copyright holder nor the names of its contributors may 
be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.