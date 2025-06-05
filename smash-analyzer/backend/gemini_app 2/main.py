import os
from dotenv import load_dotenv
from google.cloud import vision
import google.generativeai as genai
from PIL import Image
import io
from google.oauth2 import service_account

# .envファイルの読み込み
load_dotenv()

class ImageAnalyzer:
    def __init__(self, vision_credentials_path):
        """
        ImageAnalyzerクラスの初期化
        Args:
            vision_credentials_path (str): Vision API用のサービスアカウントJSONファイルのパス
        """
        # Gemini API の設定
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError(".envファイルにGOOGLE_API_KEYが設定されていません")
        
        # Vision API の認証情報設定
        credentials = service_account.Credentials.from_service_account_file(
            vision_credentials_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
            
        self.vision_client = vision.ImageAnnotatorClient(credentials=credentials)
        genai.configure(api_key=api_key)
        # 最新のGeminiモデルを使用
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_with_vision_api(self, image_path):
        """
        Google Cloud Vision APIを使用して画像を分析
        Args:
            image_path (str): 分析する画像のパス
        Returns:
            dict: 分析結果
        """
        # 画像をバイトデータとして読み込み
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        # 各種分析を実行
        results = {
            'labels': self.vision_client.label_detection(image=image).label_annotations,
            'texts': self.vision_client.text_detection(image=image).text_annotations,
            'faces': self.vision_client.face_detection(image=image).face_annotations,
            'objects': self.vision_client.object_localization(image=image).localized_object_annotations,
            'safe_search': self.vision_client.safe_search_detection(image=image).safe_search_annotation,
        }
        
        return results

    def analyze_with_gemini(self, image_path, prompt="この画像について詳しく説明してください。"):
        """
        Gemini APIを使用して画像を分析
        Args:
            image_path (str): 分析する画像のパス
            prompt (str): Geminiに送るプロンプト
        Returns:
            str: 生成された説明
        """
        image = Image.open(image_path)
        response = self.gemini_model.generate_content([prompt, image])
        return response.text

    def comprehensive_analysis(self, image_path):
        """
        Vision APIとGemini APIの両方を使用して総合的な分析を実行
        Args:
            image_path (str): 分析する画像のパス
        Returns:
            dict: 総合的な分析結果
        """
        vision_results = self.analyze_with_vision_api(image_path)
        gemini_description = self.analyze_with_gemini(image_path)

        # 結果を整形
        analysis = {
            'ラベル': [label.description for label in vision_results['labels']],
            'テキスト': [text.description for text in vision_results['texts']][:1],  # 最初の完全なテキストのみ
            '検出された物体': [obj.name for obj in vision_results['objects']],
            '顔の検出': len(vision_results['faces']),
            'セーフサーチ': {
                'アダルト': vision_results['safe_search'].adult,
                '暴力': vision_results['safe_search'].violence,
                '医療': vision_results['safe_search'].medical,
            },
            'Geminiによる説明': gemini_description
        }

        return analysis

def main():
    """
    メイン実行関数
    """
    try:
        # Vision API用の認証情報ファイルのパス
        vision_credentials_path = "/Users/takuto/gemini_app/phrasal-clover-450014-q7-5fbc72d70e0a.json"  # JSONファイルの実際のパスに変更してください
        
        analyzer = ImageAnalyzer(vision_credentials_path)
        
        # 使用例
        image_path = "/Users/takuto/gemini_app/S__75259918.jpg"  # 分析したい画像のパスに変更してください
        results = analyzer.comprehensive_analysis(image_path)
        
        # 結果の表示
        print("\n=== 画像分析結果 ===")
        for key, value in results.items():
            print(f"\n{key}:")
            if isinstance(value, list):
                for item in value:
                    print(f"- {item}")
            elif isinstance(value, dict):
                for k, v in value.items():
                    print(f"- {k}: {v}")
            else:
                print(value)

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()