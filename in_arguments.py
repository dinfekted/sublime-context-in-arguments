import sublime
import sublime_plugin
import re

from Context.base import Base

try:
  from Expression import expression
  from Statement import statement
except ImportError:
  sublime.error_message("Dependency import failed; please read readme for " +
   "Context plugin for installation instructions; to disable this " +
   "message remove this plugin")

class InArguments(Base):

  def _get_value(self, view, sel):
    nesting = expression.get_nesting(view, sel.begin(), 2048)
    if nesting == None:
      return None

    start, end = nesting[0], nesting[1]

    if sel.begin() != sel.end():
      nesting_end = expression.get_nesting(view, sel.begin(), 2048)
      if nesting_end == None:
        return None

      end_start, end_end = nesting_end[0], nesting_end[1]
      if end_start != start and end_end != end:
        return None

    previous_character = view.substr(sublime.Region(start - 2, start - 1))
    return re.search(r'[\w?!]', previous_character) != None

  def on_query_context(self, *args):
    return self._check_sel('in_arguments', self._get_value, *args)
