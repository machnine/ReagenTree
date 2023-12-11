""" Mixins for item app. """
from item.models import Item, StockItem, ItemAttachment


class ItemDetailContextMixin:
    def get_item_detail_context(self, item: Item):
        return {
            "item": item,
            "stockitems": StockItem.objects.filter(
                item=item
            ),  # TODO filter available stocks
            "attachments": ItemAttachment.objects.filter(object_id=item.id),
        }
