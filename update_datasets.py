import json

def update_dataset_file(file_path, skill_details):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for node in data['nodes']:
            skill_name = node['name']
            if skill_name in skill_details:
                detail = skill_details[skill_name]
                node['description'] = detail.get('description', '暂无描述')
                node['difficulty'] = detail.get('difficulty', '未知')
                node['learning_weeks'] = detail.get('learning_weeks', 0)
                node['resources'] = detail.get('resources', [])
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 更新成功: {file_path}")
    except Exception as e:
        print(f"❌ 更新失败 {file_path}: {e}")

def main():
    print("=" * 60)
    print("更新现有数据集文件")
    print("=" * 60)
    
    with open('skill_bank.json', 'r', encoding='utf-8') as f:
        skill_bank = json.load(f)
    
    skill_details = skill_bank.get('skill_details', {})
    
    files_to_update = [
        'data_python_fullstack.json',
        'data_java_backend.json',
        'data_data_analyst.json'
    ]
    
    for file in files_to_update:
        update_dataset_file(file, skill_details)
    
    print("\n" + "=" * 60)
    print("所有数据集更新完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
