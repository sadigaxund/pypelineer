
from .....cores.implement.ingress import Core, Type

from math import ceil

from logging import Logger, DEBUG, INFO, ERROR, WARNING

from typing import Any, Iterable, NoReturn, Union, Generator

class IngressApify(Core, Type=Type.FUNCTION):
    
    def __init__(self, apify_client, clean = False, logger: Logger = None) -> NoReturn:
        self.apify_client = apify_client
        self.clean = clean
        self.logger: Logger = logger
        super().__init__()
        
    def __call__(self, dataset_id: str) -> Any:
        self.dataset_id = dataset_id
        return self
        
    def log(self, message, level):
        if self.logger:
            self.logger.log(
                msg=message,
                level=level
            )
    
    def constructor(self):
        self.log(f"Extracting results with dataset_id='{self.dataset_id}'", INFO)
        
        metadata = self.apify_client.dataset(self.dataset_id).get()
        metadata.pop('fields', None)
        metadata.pop('schema', None)
        
        self.log(metadata, DEBUG)
        
        if metadata == None:
            raise AssertionError(f"Dataset {self.dataset_id} does not exist, skipping...")
        
        self.total_item_count = metadata['itemCount']
        self.clean_item_count = metadata['cleanItemCount']
        
        if self.total_item_count == 0:
            self.log(f"Dataset {self.dataset_id} has no items, skipping...", WARNING)
        else:
            self.log(f"Dataset has total scraped items: {self.total_item_count}", INFO)
            self.log(f"Dataset has total  clean  items: {self.clean_item_count}", INFO)
            
        self.page_size = 10000
        self.pages = ceil(self.clean_item_count / self.page_size) - 1
        self.page = 0
        
        self.total_extracted = 0
    
    def destructor(self, exc_type, exc_value, traceback):
        self.log(f"Downloaded {self.total_extracted} results from dataset ({self.dataset_id})", INFO)
    
    def available(self) -> bool:
        return self.page <= self.pages and self.total_item_count > 0
    
    def iterate(self) -> NoReturn:
        self.page += 1
        
    def produce(self) -> Union[Iterable, Any]:
        offset = self.page * self.page_size
        self.log(f"Page: {self.page + 1}/{self.pages + 1}", DEBUG)
        self.log(f"Downloading: [{offset}:{offset + self.page_size}]", DEBUG)
        
        items: Generator = self.apify_client.dataset(self.dataset_id) \
            .iterate_items(
                offset=offset,
                limit=self.page_size,
                clean=self.clean
            )
            
        for item in items:
            self.total_extracted += 1
            yield item