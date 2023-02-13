# 秋英控制台 Qiuying Console

## Road Map

## Development

### 视图函数

以 `class` 方式组织视图函数，通过请求方法区分对资源的不同操作。详情参考 `views/pet.py`，以下列一下基本思路。

| Method | Description  | Status Code When Success | Example                                                | Example Description |
| ------ | ------------ | ------------------------ | ------------------------------------------------------ | ------------------- |
| GET    | 查看         | 200                      | /pet/a-pet-id -X GET                                   | 获取某个 Pet 信息   |
| POST   | 新增         | 201                      | /pet -X GET -d '{"name": "foo", "gender": 0}'          | 新增一个 Pet        |
| PUT    | 全属性更新   | 200                      | /pet/a-pet-id -X PUT -d '{"name": "bar", "gender": 0}' | 更新某个 Pet 信息   |
| PATCH  | 部分属性更新 | 200                      | /pet/a-pet-id -X PATCH -d '{"name": "quz"}'            | 只更新 Pet 名称     |
| DELETE | 删除         | 204                      | /pet/a-pet-id -X DELETE                                | 删除某 Pet          |

## Caveats
