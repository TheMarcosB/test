from lib import Style
jump = ('-' * 50) + '\n//'

color = Style.Color('#333')
print(jump, 'color:', color)
print(jump, 'hex:', color.hex)
print(jump, 'hexa:', color.hexa)
print(jump, 'rgb:', color.rgb)
print(jump, 'rgba:', color.rgba, '\n\n')

color = Style.Alpha(color, '0.9')
print(jump, 'alpha(0.9) in color:', color)
print(jump, 'hex:', color.hex)
print(jump, 'hexa:', color.hexa)
print(jump, 'rgb:', color.rgb)
print(jump, 'rgba:', color.rgba, '\n\n')

color = Style.Color('rgb(35, 45, 55)')
print(jump, 'color:', color)
print(jump, 'hex:', color.hex)
print(jump, 'hexa:', color.hexa)
print(jump, 'rgb:', color.rgb)
print(jump, 'rgba:', color.rgba, '\n\n')

color = Style.Color('rgba(35, 45, 55, 200)')
print(jump, 'color:', color)
print(jump, 'hex:', color.hex)
print(jump, 'hexa:', color.hexa)
print(jump, 'rgb:', color.rgb)
print(jump, 'rgba:', color.rgba, '\n\n')

# mix
mix_string = 'mix(#00ff00, #0000ff)'
mix_call = Style.Eval(mix_string, 100)
print(jump, 'mix exemple:', mix_string, '= rgba {', mix_call.rgba, '}, hexa {',  mix_call.hexa, '}')

# alpha
alpha_string = 'alpha(#00ff00, 0.2)'
alpha_call = Style.Eval(alpha_string, 100)
print(jump, 'alpha exemple:', alpha_string, '= rgba {', alpha_call.rgba, '}, hexa {',  alpha_call.hexa, '}')

# calculate
calculate_string = 'calc((100px * 5) - 20px + 100%) 10%'
calculate_call = Style.Eval(calculate_string, 100)
print(jump, 'calculate exemple:', calculate_string, '=', calculate_call)

# percentage
percentage_string = '480.0px 30%'
percentage_call = Style.Eval(percentage_string, 100)
print(jump, 'percentage exemple: ', percentage_string, '=', percentage_call)

# url
url_string = 'url(http://google.com)'
url_call = Style.Eval(url_string)
print(jump, 'url exemple: ', url_string, '=', url_call)

print(Style.Url.open('https://3.bp.blogspot.com/-AvsjPdgLuWs/WJf09TPLoHI/AAAAAAAAqmE/U0IxecCwP_wN8FdmDbXkIySHBL0ijDfogCLcB/s640/Aluguel-Carro-Viagem-Economizar.jpg'))
