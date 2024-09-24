
from .html2table import jiuyangongshe
import click


@click.command()
@click.argument('date', type=str)
def get_page(date: str) -> None:
    # extract the last piece of the url as the output file name
    worker = jiuyangongshe(date)
    worker.save_page()
    worker.html2table()
    import os
    if os.path.exists(worker.output):    
        print("xlsx generated: ", worker.output)

    