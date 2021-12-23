# © 2016-2018 Eneldo Serrata <eneldo@marcos.do>
# © 2017-2018 Gustavo Valverde <gustavo@iterativo.do>

# This file is part of NCF Manager.

# NCF Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# NCF Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with NCF Manager.  If not, see <https://www.gnu.org/licenses/>.

import re
from odoo import api, fields, models
from tempfile import TemporaryFile
import base64

import logging

_logger = logging.getLogger(__name__)

try:
    import openpyxl
except (ImportError, IOError) as err:
    _logger.debug(err)

CURRENCY_DISPLAY_PATTERN = re.compile(r'(\w+)\s*(?:\((.*)\))?')


class Currency(models.Model):
    _inherit = "res.currency"

    bc_rate_xls = fields.Binary(string=u"Histórico en Excel de Tasas del Banco"
                                " Central")


    def update_rate_from_files(self):
        month_dict = {
            "Ene": "01",
            "Feb": "02",
            "Mar": "03",
            "Abr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Ago": "08",
            "Sep": "09",
            "Sept": "09",
            "Oct": "10",
            "Nov": "11",
            "Dic": "12"
        }

        self.env["res.currency.rate"].search([('currency_id', '=', 3)
                                              ]).unlink()

        file = base64.b64decode(self.bc_rate_xls)
        excel_fileobj = TemporaryFile('wb+')
        excel_fileobj.write(file)
        excel_fileobj.seek(0)
        # Create workbook
        workbook = openpyxl.load_workbook(excel_fileobj, data_only=True)
        # Get the first sheet of excel file
        sheet = workbook[workbook.sheetnames[0]]

        for row in sheet.rows:
            if row[0].row in (1, 2, 3):
                continue
            if row[0].value is None:
                break
            year = str(row[0].value)
            month = month_dict[row[1].value.strip()]
            day = str(row[2].value).zfill(2)
            name = "{}-{}-{}".format(year, month, day)
            rate = float(row[4].value)
            self.env["res.currency.rate"].create({
                "name": name,
                "rate": 1 / rate,
                "currency_id": 3
            })
            _logger.info("USD rate created {}".format(name))

class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"


    @api.depends("rate")
    def _get_converted(self):
        for rec in self:
            if rec.rate > 0:
                rec.converted = 1 / rec.rate

    converted = fields.Float(compute=_get_converted, digits=(12, 4))


    def name_get(self):
        result = []
        for rate in self:
            result.append(
                (rate.id, "{} | Tasa: {}".format(rate.name, rate.converted)))
        return result

    rate = fields.Float(
        digits=(12, 12),
        help='The rate of the currency to the currency of rate 1')
