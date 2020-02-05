base_wait = 0.0021
byte_wait = 12 / 1e6
heating_interval = 2
heating_time = 80

Defaults = {
	#maximum printing speed is listed as 60mm/s
	#each dot line is 0.125mm. 60/0.125=480 lines per second
	#1s / 480 = 0.00208 = ~0.0021
	"base_wait" : base_wait,
	"byte_wait" : byte_wait,
	"heating_points" : 9,
	"heating_time" : heating_time,
	"heating_interval" : heating_interval,
	"wait" : base_wait + \
			((heating_time * 10) / 1e6) + \
			((heating_interval * 10) / 1e6),
	"column" : 0,
	"max_column" : 32,
	"char_height" : 1,
	"char_width" : 1,
	"margin" : 0,
	"chinese_mode" : False,
	"chinese_format" : 'gb2312',
	"encoding" : "utf-8",
	"tab" : 0,
	"row_spacing" : 32,
	"overheat_sleep" : 2,
	"retries" : 10,
	"written" : 0,
	"inverse" : False,
	"rotate" : False,
	"font_b" : False,
	"bold" : False,
	"line_spacing" : 0,
	"upside_down" : False,
	"underline" : 0,
	"alignment" : 0

}