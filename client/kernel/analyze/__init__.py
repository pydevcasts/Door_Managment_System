from client.kernel.analyze.Analyzer1000 import analyzer1000
from client.kernel.analyze.Analyzer1050 import analyzer1050
from client.kernel.analyze.Analyzer1503 import analyzer1503
from client.kernel.analyze.AnalyzerFactory import analyzerFactory

# default analyzers.

analyzerFactory.register(analyzer1000)
analyzerFactory.register(analyzer1050)
analyzerFactory.register(analyzer1503)
