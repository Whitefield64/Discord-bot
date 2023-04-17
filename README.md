# Discord-bot-development
![Architecture](img/Bot_architecture.png)
## Intro
The bot has two type of components, a **consumer** and and some **aggregators**. Every aggregator subscribes to the graph of interest and formats any updated data before putting it back into the database, in the Discord message graph. The consumer subscribes to the Discord message graph and, whenever the aggregator updates a message, formats and sends it to Discord.
## Configuration

## Deployment
