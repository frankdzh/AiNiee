import re
from types import SimpleNamespace

from Base.Base import Base
from ModuleFolders.TaskExecutor import TranslatorUtil
from ModuleFolders.TaskConfig.TaskConfig import TaskConfig
from ModuleFolders.PromptBuilder.PromptBuilderEnum import PromptBuilderEnum
class PromptBuilder(Base):
    def __init__(self) -> None:
        super().__init__()

    # 获取默认系统提示词(未处理的)，优先从内存中读取，如果没有，则从文件中读取
    def get_system_default(config: TaskConfig, prompt_preset) -> str:
        if getattr(PromptBuilder, "common_system_zh", None) == None:
            with open("./Resource/Prompt/Translate/common_system_zh.txt", "r", encoding = "utf-8") as reader:
                PromptBuilder.common_system_zh = reader.read().strip()
        if getattr(PromptBuilder, "common_system_en", None) == None:
            with open("./Resource/Prompt/Translate/common_system_en.txt", "r", encoding = "utf-8") as reader:
                PromptBuilder.common_system_en = reader.read().strip()
        if getattr(PromptBuilder, "cot_system_zh", None) == None:
            with open("./Resource/Prompt/Translate/cot_system_zh.txt", "r", encoding = "utf-8") as reader:
                PromptBuilder.cot_system_zh = reader.read().strip()
        if getattr(PromptBuilder, "cot_system_en", None) == None:
            with open("./Resource/Prompt/Translate/cot_system_en.txt", "r", encoding = "utf-8") as reader:
                PromptBuilder.cot_system_en = reader.read().strip()
        if getattr(PromptBuilder, "think_system_zh", None) == None:
            with open("./Resource/Prompt/Translate/think_system_zh.txt", "r", encoding = "utf-8") as reader:
                PromptBuilder.think_system_zh = reader.read().strip()
        if getattr(PromptBuilder, "think_system_en", None) == None:
            with open("./Resource/Prompt/Translate/think_system_en.txt", "r", encoding = "utf-8") as reader:
                PromptBuilder.think_system_en = reader.read().strip()


        # 如果输入的是字典，则转换为命名空间
        if isinstance(config, dict):
            namespace = SimpleNamespace()
            for key, value in config.items():
                setattr(namespace, key, value)
            config = namespace

        # 构造结果
        if prompt_preset == PromptBuilderEnum.COMMON and config.target_language in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.common_system_zh
        elif prompt_preset == PromptBuilderEnum.COMMON and config.target_language not in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.common_system_en
        elif prompt_preset == PromptBuilderEnum.COT and config.target_language in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.cot_system_zh
        elif prompt_preset == PromptBuilderEnum.COT and config.target_language not in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.cot_system_en
        elif prompt_preset == PromptBuilderEnum.THINK and config.target_language in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.think_system_zh
        elif prompt_preset == PromptBuilderEnum.THINK and config.target_language not in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.think_system_en
        else:
            result = PromptBuilder.common_system_zh

        return result

    # 获取系统提示词(处理好的)
    def build_system(config: TaskConfig, source_lang: str) -> str:
        # 获取默认系统提示词
        PromptBuilder.get_system_default(config, "")

        # 语言信息转换
        en_sl, source_language, en_tl, target_language = TranslatorUtil.get_language_display_names(source_lang, config.target_language)

        # 构造结果
        if config == None:
            result = PromptBuilder.common_system_zh
        elif config.translation_prompt_selection["last_selected_id"] == PromptBuilderEnum.COMMON and config.target_language in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.common_system_zh
        elif config.translation_prompt_selection["last_selected_id"] == PromptBuilderEnum.COMMON and config.target_language not in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.common_system_en
            source_language = en_sl
            target_language = en_tl
        elif config.translation_prompt_selection["last_selected_id"] == PromptBuilderEnum.COT and config.target_language in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.cot_system_zh
        elif config.translation_prompt_selection["last_selected_id"] == PromptBuilderEnum.COT and config.target_language not in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.cot_system_en
            source_language = en_sl
            target_language = en_tl
        elif config.translation_prompt_selection["last_selected_id"] == PromptBuilderEnum.THINK and config.target_language in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.think_system_zh
        elif config.translation_prompt_selection["last_selected_id"] == PromptBuilderEnum.THINK and config.target_language not in ("chinese_simplified", "chinese_traditional"):
            result = PromptBuilder.think_system_en
            source_language = en_sl
            target_language = en_tl


        return result.replace("{source_language}", source_language).replace("{target_language}", target_language).strip()

    # 构建翻译示例
    def build_translation_sample(config: TaskConfig, input_dict: dict, source_lang) -> tuple[str, str]:
        list1 = []
        list3 = []
        list2 = []
        list4 = []

        conv_source_lang = TranslatorUtil.map_language_code_to_name(source_lang)
        if conv_source_lang == 'un':
            return "", ""
            #conv_source_lang = TranslatorUtil.map_language_code_to_name(source_lang.most_common)

        # 检测原文语言是否能够构建动态示例
        if conv_source_lang not in ["japanese", "korean", "russian", "chinese_simplified", "chinese_traditional", "french",
                                "german", "spanish", "english"]:
            return "", ""

        # 获取自适应示例（无法构建english的）
        if conv_source_lang in ["japanese", "korean", "russian", "chinese_simplified", "chinese_traditional", "french",
                                "german", "spanish"]:
            list2, list4 = PromptBuilder.build_adaptive_translation_sample(config, input_dict, conv_source_lang)

        # 将两个列表合并
        combined_list = list1 + list2
        combined_list2 = list3 + list4

        # 如果前面都没能构成动态示例，则根据语言添加基础示例
        if not combined_list:
            base_example = {
                "base": {
                    "japanese": "例示テキスト",
                    "korean": "예시 텍스트",
                    "russian": "Пример текста",
                    "chinese_simplified": "示例文本",
                    "chinese_traditional": "翻譯示例文本",
                    "english": "Sample Text",
                    "spanish": "Texto de ejemplo",
                    "french": "Exemple de texte",
                    "german": "Beispieltext",
                }
            }

            # 如果没有对应的示例语言，默认使用英文
            source_base_example = base_example["base"].get(conv_source_lang, "Sample Text")
            combined_list.append(source_base_example)
            combined_list2.append(base_example["base"][config.target_language])

        # 限制示例总数量为3个，如果多了，则从最后往前开始削减
        if len(combined_list) > 3:
            combined_list = combined_list[:3]
            combined_list2 = combined_list2[:3]

        # 创建空字典
        source_dict = {}
        target_dict = {}
        source_str = ""
        target_str = ""

        # 遍历合并后的列表，并创建键值对
        for index, value in enumerate(combined_list):
            source_dict[str(index)] = value
        for index, value in enumerate(combined_list2):
            target_dict[str(index)] = value

        # 将原文本字典转换成行文本，并加上数字序号
        if source_dict:

            # 构建原文示例
            numbered_lines = []
            for index, line in enumerate(source_dict.values()):
                # 检查是否为多行文本
                if "\n" in line:
                    lines = line.split("\n")
                    numbered_text = f"{index + 1}.[\n"
                    total_lines = len(lines)
                    for sub_index, sub_line in enumerate(lines):
                        numbered_text += f'"{index + 1}.{total_lines - sub_index}.,{sub_line}",\n'
                    numbered_text = numbered_text.rstrip('\n')
                    numbered_text = numbered_text.rstrip(',')
                    numbered_text += f"\n]"  # 用json.dumps会影响到原文的转义字符
                    numbered_lines.append(numbered_text)
                else:
                    # 单行文本直接添加序号
                    numbered_lines.append(f"{index + 1}.{line}")

            source_str = "\n".join(numbered_lines)


            # 构建译文示例
            target_numbered_lines = []
            for index, line in enumerate(target_dict.values()):
                # 检查是否为多行文本
                if "\n" in line:
                    lines = line.split("\n")
                    numbered_text = f"{index + 1}.[\n"
                    total_lines = len(lines)
                    for sub_index, sub_line in enumerate(lines):
                        numbered_text += f'"{index + 1}.{total_lines - sub_index}.,{sub_line}",\n'
                    numbered_text = numbered_text.rstrip('\n')
                    numbered_text = numbered_text.rstrip(',')
                    numbered_text += f"\n]"  # 用json.dumps会影响到原文的转义字符
                    target_numbered_lines.append(numbered_text)
                else:
                    # 单行文本直接添加序号
                    target_numbered_lines.append(f"{index + 1}.{line}")


            target_str = "\n".join(target_numbered_lines)



        return source_str, target_str

    # 辅助函数，清除列表过多相似的元素
    def clean_list(lst) -> list[str]:
        # 函数用于删除集合中的数字
        def remove_digits(s) -> set:
            return set(filter(lambda x: not x.isdigit(), s))

        # 函数用于计算两个集合之间的差距
        def set_difference(s1, s2) -> int:
            return len(s1.symmetric_difference(s2))

        # 删除每个元素中的数字，并得到一个由集合组成的列表
        sets_list = [remove_digits(s) for s in lst]

        # 初始化聚类列表
        clusters = []

        # 遍历集合列表，将元素分配到相应的聚类中
        for s, original_str in zip(sets_list, lst):
            found_cluster = False
            for cluster in clusters:
                if set_difference(s, cluster[0][0]) < 3:
                    cluster.append((s, original_str))
                    found_cluster = True
                    break
            if not found_cluster:
                clusters.append([(s, original_str)])

        # 从每个聚类中提取一个元素，组成新的列表
        result = [cluster[0][1] for cluster in clusters]

        return result

    # 辅助函数，重新调整列表中翻译示例的后缀数字
    def replace_and_increment(items, prefix) -> list[str]:
        pattern = re.compile(r"{}(\d{{1,2}})".format(re.escape(prefix)))  # 使用双括号来避免KeyError
        result = []  # 用于存储结果的列表
        n = 0
        p = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        for item in items:
            if pattern.search(item):  # 如果在元素中找到匹配的模式
                new_item = item
                j = 1  # 初始化 j
                while True:

                    # 正则匹配
                    match = pattern.search(new_item)

                    # 如果没有匹配到，退出
                    if not match:
                        break

                    # 防止列表循环越界
                    if n >= 24:
                        #print("bug")
                        n = 0

                    # 替换示例文本后缀
                    new_item = new_item[:match.start()] + f"{prefix}{p[n]}-{j}" + new_item[match.end():]

                    # 在每次替换后递增 j
                    j += 1

                # 替换完之后添加进结果列表
                result.append(new_item)

                # 变量n递增
                n += 1
            else:
                result.append(item)  # 如果没有匹配，将原始元素添加到结果列表

        return result  # 返回修改后的列表

    # 构建相似格式翻译示例
    def build_adaptive_translation_sample(config: TaskConfig, input_dict: dict, conv_source_lang: str) -> tuple[list[str], list[str]]:
        # 输入字典示例
        # ex_dict = {
        #     "0": "こんにちは，こんにちは。こんにちは#include <iostream>",
        #     "1": "55345こんにちは",
        #     "2": "こんにちはxxxx！",
        #     "3": "こんにちは",
        # }

        # 输出列表1示例
        # ex_dict = [
        #     "原文テキストA-1，原文テキストA-2。原文テキストA-3#include <iostream>",
        #     "55345原文テキストB-1",
        #     "原文テキストC-1xxxx！",
        # ]

        # 输出列表2示例
        # ex_dict = [
        #     "译文文本A-1，译文文本A-2。译文文本A-3#include <iostream>",
        #     "55345译文文本B-1",
        #     "译文文本C-1xxxx！",
        # ]

        # 定义不同语言的正则表达式
        patterns_all = {
            "japanese": re.compile(
                r"["
                r"\u3041-\u3096"  # 平假名
                r"\u30A0-\u30FF"  # 片假名
                r"\u4E00-\u9FAF"  # 汉字
                "]+",
                re.UNICODE,
            ),
            "korean": re.compile(r"[\uAC00-\uD7AF]+", re.UNICODE),  # 韩文字母
            "russian": re.compile(r"[\u0400-\u04FF]+", re.UNICODE),  # russian字母
            "chinese_simplified": re.compile(r"[\u4E00-\u9FA5]+", re.UNICODE),  # 简体中文
            "chinese_traditional": re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]+", re.UNICODE),
            "spanish": re.compile(
                r"[a-zA-ZÁÉÍÓÚÑáéíóúñÜü]+",  # 覆盖spanish特殊字符
                re.UNICODE
            ),
            "french": re.compile(
                r"[a-zA-ZÀ-ÿ]+",  # 覆盖所有法语重音字符
                re.UNICODE
            ),
            "german": re.compile(
                r"[a-zA-ZÄÖÜäöüß]+",  # 德语特殊字符
                re.UNICODE
            ),
        }

        # 定义不同语言的翻译示例（新增三种语言）
        text_all = {
            "japanese": "例示テキスト",
            "korean": "예시 텍스트",
            "russian": "Пример текста",
            "chinese_simplified": "示例文本",
            "chinese_traditional": "翻譯示例文本",
            "english": "Sample Text",
            "spanish": "Texto de ejemplo",
            "french": "Exemple de texte",
            "german": "Beispieltext",
        }

        # 根据输入选择正则表达式与翻译文本
        pattern = patterns_all[conv_source_lang]
        source_text = text_all[conv_source_lang]
        translated_text = text_all[config.target_language]

        source_list, translated_list = [], []
        counter = 1  # 统一计数器保证编号同步

        for value in input_dict.values():
            if pattern.search(value):
                # 使用相同计数器生成编号
                src = pattern.sub(lambda _: f"{source_text}{counter}", value)
                trans = pattern.sub(lambda _: f"{translated_text}{counter}", value)
                source_list.append(src)
                translated_list.append(trans)
                counter += 1

        # 优化过滤逻辑
        def filter_func(items, text):
            return [item for item in items 
                    if (not item.startswith(text)  # 排除纯示例开头的项
                        or not any(c.isdigit() for c in item[-3:]))  # 排除末尾3字符含数字的项
                    and len(item) <= 80]  #过滤不超过设定长度的项

        # 清理和重新编号
        source_cleaned = PromptBuilder.clean_list(filter_func(source_list, source_text))
        trans_cleaned = PromptBuilder.clean_list(filter_func(translated_list, translated_text))

        # 最终编号处理
        return (
            PromptBuilder.replace_and_increment(source_cleaned, source_text),
            PromptBuilder.replace_and_increment(trans_cleaned, translated_text)
        )

    # 构建原文
    def build_source_text(config: TaskConfig, source_text_dict: dict) -> str:
        numbered_lines = []
        for index, line in enumerate(source_text_dict.values()):
            # 检查是否为多行文本
            if "\n" in line:
                lines = line.split("\n")  # 需要与回复提取的行分割方法一致
                numbered_text = f"{index + 1}.[\n"
                total_lines = len(lines)
                for sub_index, sub_line in enumerate(lines):
                    # 不去除空白内容，保留\r其他平台的换行符，虽然AI回复不一定保留...
                    # 仅当 **只有一个** 尾随空格时才去除
                    sub_line = sub_line[:-1] if re.match(r'.*[^ ] $', sub_line) else sub_line
                    numbered_text += f'"{index + 1}.{total_lines - sub_index}.,{sub_line}",\n'
                numbered_text = numbered_text.rstrip('\n')
                numbered_text = numbered_text.rstrip(',')
                numbered_text += f"\n]"  # 用json.dumps会影响到原文的转义字符
                numbered_lines.append(numbered_text)
            else:
                # 单行文本直接添加序号
                numbered_lines.append(f"{index + 1}.{line}")

        source_text_str = "\n".join(numbered_lines)
        
        return source_text_str

    # 构造术语表
    def build_glossary_prompt(config: TaskConfig, input_dict: dict) -> str:
        # 将输入字典中的所有值转换为集合
        lines = set(line for line in input_dict.values())

        # 筛选在输入词典中出现过的条目
        result = []
        for v in config.prompt_dictionary_data:
            src_lower = v.get("src").lower() # 将术语表中的 src 转换为小写
            if any(src_lower in line.lower() for line in lines): # 将原文行也转换为小写进行比较
                result.append(v)

        # 数据校验
        if len(result) == 0:
            return ""

        # 避免空的默认内容
        if len(result) == 1 and (result[0]["src"] == ""):
            return ""

        # 初始化变量，以免出错
        glossary_prompt_lines = []

        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            # 添加开头
            glossary_prompt_lines.append(
                "\n###术语表"
                + "\n" + "原文|译文|备注"
            )

            # 添加数据
            for v in result:
                glossary_prompt_lines.append(f"{v.get("src")}|{v.get("dst")}|{v.get("info") if v.get("info") != "" else " "}")

        else:
            # 添加开头
            glossary_prompt_lines.append(
                "\n###Glossary"
                + "\n" + "Original Text|Translation|Remarks"
            )

            # 添加数据
            for v in result:
                glossary_prompt_lines.append(f"{v.get("src")}|{v.get("dst")}|{v.get("info") if v.get("info") != "" else " "}")


        # 拼接成最终的字符串
        glossary_prompt = "\n".join(glossary_prompt_lines)

        return glossary_prompt

    # 构造禁翻表
    def build_ntl_prompt(config: TaskConfig, source_text_dict) -> str:

        # 获取禁翻表内容
        exclusion_list_data = config.exclusion_list_data.copy()


        exclusion_dict = {}  # 用字典存储并自动去重
        texts = list(source_text_dict.values())
        
        # 处理正则匹配
        for element in exclusion_list_data:
            regex = element.get("regex", "").strip()
            marker = element.get("markers", "").strip()
            info = element.get("info", "")
            
            # 检查是否写正则，如果写了，只处理正则
            if regex:
                # 避免错误正则，导致崩溃
                try:
                    # 编译正则表达式字符串为模式对象
                    pattern = re.compile(regex)
                    # 寻找文本中所有符合正则的文本内容
                    for text in texts:
                        for match in pattern.finditer(text):
                            markers = match.group(0)
                            # 避免重复添加
                            if markers not in exclusion_dict: 
                                exclusion_dict[markers] = info
                except re.error:
                    pass
            # 没写正则，只处理标记符        
            else:
                found = any(marker in text for text in texts)
                if found and marker not in exclusion_dict:  # 避免重复添加
                    exclusion_dict[marker] = info
        
        # 检查内容是否为空
        if not exclusion_dict :
            return ""

        # 构建结果字符串
        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            result = "\n###禁翻表，以下特殊标记符无需翻译"+ "\n特殊标记符|备注"
        else:
            result = "\n###Non-Translation List,Leave the following marked content untranslated"+ "\nSpecial marker|Remarks"

        for markers, info in exclusion_dict.items():
            result += f"\n{markers}|{info}" if info else f"\n{markers}|"
        
        return result

    # 构造角色设定
    def build_characterization(config: TaskConfig, input_dict: dict) -> str:
        # 将数据存储到中间字典中
        dictionary = {}
        for v in config.characterization_data:
            dictionary[v.get("original_name", "")] = v

        # 筛选，如果该key在发送文本中，则存储进新字典中
        temp_dict = {}
        for key_a, value_a in dictionary.items():
            for _, value_b in input_dict.items():
                if key_a in value_b:
                    temp_dict[key_a] = value_a

        # 如果没有含有字典内容
        if temp_dict == {}:
            return ""

        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            profile = "\n###角色介绍"
            for key, value in temp_dict.items():
                original_name = value.get("original_name")
                translated_name = value.get("translated_name")
                gender = value.get("gender")
                age = value.get("age")
                personality = value.get("personality")
                speech_style = value.get("speech_style")
                additional_info = value.get("additional_info")

                profile += f"\n【{original_name}】"
                if translated_name:
                    profile += f"\n- 译名：{translated_name}"

                if gender:
                    profile += f"\n- 性别：{gender}"

                if age:
                    profile += f"\n- 年龄：{age}"

                if personality:
                    profile += f"\n- 性格：{personality}"

                if speech_style:
                    profile += f"\n- 说话方式：{speech_style}"

                if additional_info:
                    profile += f"\n- 补充信息：{additional_info}"

                profile += "\n"

        else:
            profile = "\n###Character Introduction"
            for key, value in temp_dict.items():
                original_name = value.get("original_name")
                translated_name = value.get("translated_name")
                gender = value.get("gender")
                age = value.get("age")
                personality = value.get("personality")
                speech_style = value.get("speech_style")
                additional_info = value.get("additional_info")

                profile += f"\n【{original_name}】"
                if translated_name:
                    profile += f"\n- Translated_name：{translated_name}"

                if gender:
                    profile += f"\n- Gender：{gender}"

                if age:
                    profile += f"\n- Age：{age}"

                if personality:
                    profile += f"\n- Personality：{personality}"

                if speech_style:
                    profile += f"\n- Speech_style：{speech_style}"

                if additional_info:
                    profile += f"\n- Additional_info：{additional_info}"

                profile += "\n"

        return profile

    # 构造背景设定
    def build_world_building(config: TaskConfig) -> str:
        # 获取自定义内容
        world_building = config.world_building_content

        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            profile = "\n###背景设定"

            profile += f"\n{world_building}\n"

        else:
            profile = "\n###Background Setting"

            profile += f"\n{world_building}\n"

        return profile

    # 构造文风要求
    def build_writing_style(config: TaskConfig) -> str:
        # 获取自定义内容
        writing_style = config.writing_style_content

        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            profile = "\n###翻译风格"

            profile += f"\n{writing_style}\n"

        else:
            profile = "\n###Writing Style"

            profile += f"\n{writing_style}\n"

        return profile

    # 构建翻译示例
    def build_translation_example(config: TaskConfig) -> str:
        data = config.translation_example_data

        # 数据校验
        if len(data) == 0:
            return ""

        # 构建翻译示例字符串
        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            translation_example = "\n###翻译示例\n"

        else:
            translation_example = "\n###Translation Example\n"

        for index, pair in enumerate(data, start=1):
            # 使用解构赋值提升可读性
            original = pair.get("src", "")
            translated = pair.get("dst", "")

            # 添加换行符（首行之后才添加）
            if index > 1:
                translation_example += "\n"

            # 使用更严谨的字符串格式化
            if config.target_language in ("chinese_simplified", "chinese_traditional"):
                translation_example += f"  -原文{index}：{original}\n  -译文{index}：{translated}"

            else:
                translation_example += f"  -Original {index}: {original}\n  -Translation {index}: {translated}"

        return translation_example

    # 携带原文上文
    def build_pre_text(config: TaskConfig, input_list: list[str]) -> str:
        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            profile = "###上文内容\n"
            profile += "<previous>\n"

        else:
            profile = "###Previous text\n"
            profile += "<previous>\n"

        # 使用列表推导式，转换为字符串列表
        formatted_rows = [item for item in input_list]

        # 使用换行符将列表元素连接成一个字符串
        profile += f"{"\n".join(formatted_rows)}\n"

        profile += "</previous>\n"

        return profile

    # 构建用户示例前文
    def build_userExamplePrefix(config: TaskConfig) -> str:
        # 根据中文开关构建
        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            profile = "###这是你接下来的翻译任务，原文文本如下\n"
        else:
            profile = "###This is your next translation task, the original text is as follows\n"

        return profile

    # 构建模型示例前文
    def build_modelExamplePrefix(config: TaskConfig) -> str:
        # 根据中文开关构建
        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            # 非cot的构建
            profile = "我完全理解了翻译的要求与原则，我将遵循您的指示进行翻译，以下是对原文的翻译:\n"

        else:
            # Non-CoT prompt construction
            profile = "I have fully understood the translation requirements and principles. I will follow your instructions to perform the translation. Below is my translation of the original text:\n"

        return profile

    # 构建翻译前文:
    def build_userQueryPrefix(config: TaskConfig) -> str:
        # 根据中文开关构建
        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            profile = " ###这是你接下来的翻译任务，原文文本如下\n"
        else:
            profile = " ###This is your next translation task, the original text is as follows\n"
        return profile

    # 构建预输入回复的前文
    def build_modelResponsePrefix(config: TaskConfig) -> str:
        # 根据中文开关构建
        if config.target_language in ("chinese_simplified", "chinese_traditional"):
            profile = "我完全理解了翻译的要求与原则，我将遵循您的指示进行翻译，以下是对原文的翻译:"
            profile_cot = "我完全理解了翻译的步骤与原则，我将遵循您的指示进行翻译，并深入思考和解释:"
        else:
            profile = "I have fully understood the translation requirements and principles. I will follow your instructions to perform the translation. Below is my translation of the original text:"
            profile_cot = "I have fully understood the steps and principles of translation. I will follow your instructions to perform the translation and provide in-depth thinking and explanations:"

        # 根据cot开关进行选择
        if config.translation_prompt_selection["last_selected_id"] == PromptBuilderEnum.COT:
            the_profile = profile_cot
        else:
            the_profile = profile

        return the_profile


    # 生成信息结构 - 通用
    def generate_prompt(config, source_text_dict: dict, previous_text_list: list[str], source_lang) -> tuple[list[dict], str, list[str]]:
        # 储存指令
        messages = []
        # 储存额外日志
        extra_log = []

        # 基础系统提示词
        if config.translation_prompt_selection["last_selected_id"] in (PromptBuilderEnum.COMMON, PromptBuilderEnum.COT, PromptBuilderEnum.THINK):
            system = PromptBuilder.build_system(config, source_lang)
        else:
            system = config.translation_prompt_selection["prompt_content"]  # 自定义提示词


        # 如果开启术语表
        if config.prompt_dictionary_switch == True:
            glossary = PromptBuilder.build_glossary_prompt(config, source_text_dict)
            if glossary != "":
                system += glossary
                extra_log.append(glossary)

        # 如果开启禁翻表
        if config.exclusion_list_switch == True:
            ntl = PromptBuilder.build_ntl_prompt(config, source_text_dict)
            if ntl != "":
                system += ntl
                extra_log.append(ntl)


        # 如果角色介绍开关打开
        if config.characterization_switch == True:
            characterization = PromptBuilder.build_characterization(config, source_text_dict)
            if characterization != "":
                system += characterization
                extra_log.append(characterization)

        # 如果启用自定义世界观设定功能
        if config.world_building_switch == True:
            world_building = PromptBuilder.build_world_building(config)
            if world_building != "":
                system += world_building
                extra_log.append(world_building)

        # 如果启用自定义行文措辞要求功能
        if config.writing_style_switch == True:
            writing_style = PromptBuilder.build_writing_style(config)
            if writing_style != "":
                system += writing_style
                extra_log.append(writing_style)

        # 如果启用翻译风格示例功能
        if config.translation_example_switch == True:
            translation_example = PromptBuilder.build_translation_example(config)
            if translation_example != "":
                system += translation_example
                extra_log.append(translation_example)

        # 构建动态few-shot
        switch_A = config.few_shot_and_example_switch # 打开动态示例开关时
        switch_B = config.translation_prompt_selection["last_selected_id"] == PromptBuilderEnum.COMMON #仅在通用提示词
        if switch_A and switch_B:

            # 获取默认示例前置文本
            pre_prompt_example = PromptBuilder.build_userExamplePrefix(config)
            fol_prompt_example = PromptBuilder.build_modelExamplePrefix(config)

            # 获取具体动态示例内容
            original_exmaple, translation_example_content = PromptBuilder.build_translation_sample(config, source_text_dict, source_lang)
            if original_exmaple and translation_example_content:
                messages.append({
                    "role": "user",
                    "content": f"{pre_prompt_example}<textarea>\n{original_exmaple}\n</textarea>"
                })
                messages.append({
                    "role": "assistant",
                    "content": f"{fol_prompt_example}<textarea>\n{translation_example_content}\n</textarea>"
                })
                extra_log.append(f"原文示例已添加：\n{original_exmaple}")
                extra_log.append(f"译文示例已添加：\n{translation_example_content}")

        # 如果加上文，获取上文内容
        previous = ""
        if config.pre_line_counts and previous_text_list:
            previous = PromptBuilder.build_pre_text(config, previous_text_list)
            if previous != "":
                extra_log.append(f"###上文内容\n{"\n".join(previous_text_list)}")


        # 构建待翻译文本
        source_text = PromptBuilder.build_source_text(config,source_text_dict)
        pre_prompt = PromptBuilder.build_userQueryPrefix(config) # 用户提问前置文本
        source_text_str = f"{previous}\n{pre_prompt}<textarea>\n{source_text}\n</textarea>"

        # 构建用户信息
        messages.append(
            {
                "role": "user",
                "content": source_text_str,
            }
        )

        # 构建预输入回复信息
        switch_C = config.translation_prompt_selection["last_selected_id"] in (PromptBuilderEnum.COT, PromptBuilderEnum.COMMON) 
        if switch_A and switch_C:
            fol_prompt = PromptBuilder.build_modelResponsePrefix(config)
            messages.append({"role": "assistant", "content": fol_prompt})


        return messages, system, extra_log

