# Discord-bot-development`
![Architecture](img/Bot_architecture.png)
## Intro
The bot has two type of components, a **consumer** and and some **aggregators**. Every aggregator subscribes to the graph of interest and formats any updated data before putting it back into the database, in the Discord message graph. The consumer subscribes to the Discord message graph and, whenever the aggregator updates a message, formats and sends it to Discord.
## Configuration
First of all set your working directory to 'src'

<pre>
cd ./DiscordBot/src
</pre>

Now, bot can be configured in three ways.

- In the directory 'src' there is another one called 'resources'. In that directory there is a default JSAP file.
Open that file and configure the parametres: `host`, `sparql11protocol.port`, `saprql11seprotocol.availableProtocols.ws.port`, `TOKEN` and `CHANNEL_ID`.
- Set the five parameters as enviroment variables on your shell. Set `HOST_NAME`, `HTTP_PORT`, `WS_PORT`, `CHANNEL_ID`, `TOKEN`.
- Specify a different JSAP path, different from the default one using line arguments.   <pre>python ./yourscript.py -jsap yourpath.jsap</pre>
## Deployment
