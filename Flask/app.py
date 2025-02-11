from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
 
app = Flask(__name__)
run_with_ngrok(app)  # 运行应用程序时启动ngrok
   
   # ... （添加你的路由和应用程序逻辑） ...
from flask import Flask, render_template, request, jsonify
from io import BytesIO
import base64
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/submit-prompt', methods=['POST'])
def generate():
    prompt = request.form['prompt-input']
    
    # 使用 Stable Diffusion 生成图像
    image = pipe(prompt=prompt).images[0]
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # 使用 Flan-T5-XL 生成文本
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    generated_output = model.generate(input_ids, max_length=512)
    generated_text = tokenizer.decode(generated_output[0], skip_special_tokens=True)
    
    return render_template('index.html', generated_image=img_str, generated_text=generated_text)
   if __name__ == '__main__':
       app.run()
