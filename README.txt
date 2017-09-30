Non-terrible Tangerine data viewer

Use as:

  python tangerine_to_ofx_viewer.py clientid password

This will write a single html file named tangerine-clientid.html that doesn't
take forever to load, isn't full of enormous ugly boxes full of "insights" and
incorrect categorizations, doesn't have ridiculous huge fonts, etc.

The data is retrieved over HTTPS using Tangerine's OFX endpoint. Other
retrieving data from the Tangerine server, there is no other communication with
the network. The script writes a single html file, and does not save any other
data to any other locations.

Regrettably, Tangerine has let the OFX data source languish since they took it
over from ING Direct. In particular, RSP accounts were never integrated at all
and so will not show up, and the credit card product only reports what's on the
most recent statement, rather than the last N transactions as other account
types do. This is particularly bad right at the end of the monthly cycle, as
some data will only show up for one day before the roll over to the next
cycle.

Nevertheless, maybe it's a less frustrating tool.

There's no two-way communcation, so you can't move money or anything with this,
it's just a simple viewer.
