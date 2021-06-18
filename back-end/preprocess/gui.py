from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlFile, ControlButton, ControlCombo
from csv2owl import csv2owl


class Csv2OwlWidget(BaseWidget):
    def __init__(self):
        super(Csv2OwlWidget, self).__init__('csv2owl')

        self._prefix = ControlFile('Prefixes CSV')
        self._classes = ControlFile('Classes CSV')
        self._properties = ControlFile('Properties CSV')
        self._output_format = ControlCombo('Output Format')
        self._output_format.add_item('JSON-LD', 'json-ld')
        self._output_format.add_item('XML', 'pretty-xml')

        self._generate = ControlButton('Generate')
        self._generate.value = self.__generateAction

    def __changeOutput(self):
        print()

    def __generateAction(self):
        if not (
                self._classes.value and
                self._properties.value and
                self._prefix.value
                ):
            return
        output_file = 'output.'
        if 'json' in self._output_format.value:
            output_file += 'json'
        else:
            output_file += 'xml'

        with open(self._classes.value, 'r') as classes,\
            open(self._properties.value, 'r') as properties,\
            open(self._prefix.value, 'r') as prefix,\
            open(output_file, 'wb') as output_file:
            graph = csv2owl(classes, properties, prefix)

            output_file.write(
                    graph.serialize(format=self._output_format.value)
            )


if __name__ == "__main__":
    from pyforms import start_app
    start_app(Csv2OwlWidget)
