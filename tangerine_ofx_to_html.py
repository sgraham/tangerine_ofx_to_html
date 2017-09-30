import ofxclient
import os
import sys
import decimal

HTML_BEGIN = '''<!doctype html>
<html>
<head>
<style>
body {
  font-family: Helvetica, Arial, sans-serif;
  font-size: 10pt;
}

table {
  width: 100%;
  border-collapse: collapse;
}

td, th {
  border: 1px solid #eee;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #eee;
}

.balance {
  padding: 8px;
  margin-bottom: 8px;
}

.credit {
  background-color: #e6ffe6;
}

.debit {
  background-color: #ffe6e6;
}

.memo {
  color: #888;
  font-size: 9pt;
}
</style>
</head>
<body>
'''

HTML_END = '''
</body>
</html>
'''

TEMPLATE_ACCOUNT = '''
<h2>{description} &mdash; Account #{number} &mdash; <span class="balance {creditdebit}">{balance}</span></h2>
<table>
<tr>
  <th>Date</th>
  <th>Transaction</th>
  <th>Amount</th>
  <th>Balance</th>
  <th>Memo</th>
</tr>
{tablerows}
</table>
'''

TEMPLATE_ROW = '''
<tr>
  <td>{date}</td>
  <td>{transaction}</td>
  <td class="{creditdebit}">{amount}</td>
  <td>{balance}</td>
  <td><span class="memo">{memo}</span></td>
</tr>
'''


def AsMoney(value, places=2, curr='$', sep=',', dp='.',
             pos='+', neg='-', trailneg=''):
  q = decimal.Decimal(10) ** -places      # 2 places --> '0.01'
  sign, digits, exp = value.quantize(q).as_tuple()
  result = []
  digits = map(str, digits)
  build, next = result.append, digits.pop
  if sign:
    build(trailneg)
  for i in range(places):
    build(next() if digits else '0')
  build(dp)
  if not digits:
    build('0')
  i = 0
  while digits:
    build(next())
    i += 1
    if i == 3 and digits:
      i = 0
      build(sep)
  build(curr)
  build(neg if sign else pos)
  return ''.join(reversed(result))


def main(args):
  if len(args) != 2:
    print 'usage: <username or client id> <password>'
    return 1

  username = args[0]
  password = args[1]

  filename = 'tangerine-%s.html' % username
  with open(filename, 'w') as out:
    out.write(HTML_BEGIN)
    out.write('<h1>Tangerine data for %s</h1>' % username)

    inst = ofxclient.Institution(id='10951',
                                org='TangerineBank',
                                url='https://ofx.tangerine.ca',
                                username=username,
                                password=password)
    for account in inst.accounts():
      if isinstance(account, ofxclient.account.BankAccount):
        result = []
        statement = account.statement(100)
        cur_balance = statement.balance
        for t in statement.transactions:
          result.append([t.date.date().isoformat(), t.payee, t.amount,
                         '???', t.memo, 'credit' if t.amount >= 0 else 'debit'])
        rows = []
        for r in reversed(sorted(result)):
          r[3] = cur_balance
          cur_balance -= r[2]
          rows.append(TEMPLATE_ROW.format(
              date=r[0], transaction=r[1], amount=AsMoney(r[2]), balance=r[3],
              memo=r[4], creditdebit=r[5]))
        out.write(TEMPLATE_ACCOUNT.format(
          description=account.description,
          number=account.number,
          creditdebit='credit' if statement.balance >= 0 else 'debit',
          balance=AsMoney(statement.balance),
          tablerows='\n'.join(rows)))
      else:
        print 'ignoring non-BankAccount', account.number
    out.write(HTML_END)
  print 'Wrote %s.' % filename

  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
