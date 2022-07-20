# A LEAF User Interface with Streamlit
 
This project is based on practicing the basic examples in the [original LEAF example](https://github.com/dos-group/leaf/tree/main/examples) in python version, users can directly watch the power usage in user modified infrastructure and application chart. This application is conducted through [streamlit](https://streamlit.io/) for fast built data representing. 

Some new methods introduced in the leaf-GUI for agile and compatibility usage, as a result, users will no longer need to write [complex loops for writing to csv](https://github.com/dos-group/leaf/blob/b6a2c92cafa614f1f0adde4f5b581d9d0a461937/examples/smart_city_traffic/main.py#L56-L78) ,and [modify how each data](https://github.com/dos-group/leaf/tree/main/examples/smart_city_traffic/analysis) would be display in the final chart.

## 🚀 How does it work?

For LEAF starters, you can just input [examples](https://github.com/ZZZZZZZZZED/leaf-GUI/tree/main/examples) in the python interpreter in the home page. Click 'run simulator' and check the results.

Please do not forget to add this line for you to easily draw and classify lines in the graph for each [power meter](https://leaf.readthedocs.io/en/latest/reference/power.html).

```
import csv_handler as ch
```

To understand why we importing csv_handler, use the the original [smart_city_traffic](https://github.com/dos-group/leaf/blob/main/examples/smart_city_traffic/main.py) code snippet as an example：

Set power meters:
```python
env.process(pm_cloud.run(env))
env.process(pm_fog.run(env))
env.process(pm_wan_up.run(env))
env.process(pm_wan_down.run(env))
env.process(pm_wifi.run(env))
```
Then

Original method write results to csv:
```python
csv_content = "time,cloud static,cloud dynamic,fog static,fog dynamic,wifi static,wifi dynamic,wanUp static," \
                      "wanUp dynamic,wanDown static,wanDown dynamic\n"
for i, (cloud, fog, wifi, wan_up, wan_down) in enumerate(zip(pm_cloud.measurements, pm_fog.measurements, pm_wifi.measurements, pm_wan_up.measurements, pm_wan_down.measurements)):
csv_content += f"{i},{cloud.static},{cloud.dynamic},{fog.static},{fog.dynamic},{wifi.static},{wifi.dynamic},{wan_up.static},{wan_up.dynamic},{wan_down.static},{wan_down.dynamic}\n"
with open(f"{result_dir}/infrastructure.csv", 'w') as csvfile:
            csvfile.write(csv_content)
```

The above code block shows the efforts made in the [original script](https://github.com/dos-group/leaf/blob/b6a2c92cafa614f1f0adde4f5b581d9d0a461937/examples/smart_city_traffic/main.py#L66-L72) in order to visualize some power meters, however this code is not reusable and complex. Even with continued use of this method, some leaf simulator characteristics such as [sampling frequency](https://github.com/dos-group/leaf/blob/b6a2c92cafa614f1f0adde4f5b581d9d0a461937/leaf/power.py#L182) and [delay](https://github.com/dos-group/leaf/blob/b6a2c92cafa614f1f0adde4f5b581d9d0a461937/leaf/power.py#L200-L207) are difficult to solve while using above method.

So, a more convinent method would be:

```python
ch.output_csv(PM=pm_cloud, rename='Cloud',type = 1)
ch.output_csv(PM=pm_fog, rename='Fog',type = 1)
ch.output_csv(PM=pm_wan_up, rename='Wan up',type = 1)
ch.output_csv(PM=pm_wan_down, rename='Wan down',type = 1)
ch.output_csv(PM=pm_wifi, rename='WIFI',type = 1)
```
The output_csv method takes 3 parameters:
```
(PM = power meter instance, rename = 'name you want in the graph', type = 1 is for infrastructure type = 2 is for application)
```

Finally, don't forget to add
```python
ch.merge_results()
```

## risk
