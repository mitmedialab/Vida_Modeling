'''
MIT License

Copyright (c) 2020 Sebastian Cornejo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import pandas as pd

def prod46(fte, prod):
    print('generating prod46')
    df = pd.read_csv(fte)
    df.to_csv(prod + '.csv', index=False)

    df_t = df.T
    df_t.to_csv(prod + '_t.csv', header=False)

    identifiers = ['fecha_primeros_sintomas']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='Casos', value_name='Total')
    df_std.to_csv(prod + '_std.csv', index=False)




if __name__ == '__main__':
    prod46('../input/Curvas_epi/activos vs recuperados.csv', '../output/producto46/activos_vs_recuperados')