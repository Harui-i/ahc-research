# これはなに

私はAHCで強化学習(以下 RL)で1位を取ることを夢見ています。

そのためには、RLの推論をAtCoder環境(2s TLE, 1 CPU, 1024MiB RAM, 512KiB src)で高速に動かす必要があります。

なので、GPUを使った手法や、マルチコア前提の手法、そして 384KiB以上(base64で埋め込む場合)(FP16 で埋め込む場合は、2bytes/paramなので 192 Ki params以上) を埋め込むような手法は使えません。

そのような、特徴的な制約の中で、NNに不可欠な行列ベクトル積を高速に動かす方法を模索するリポジトリです。


# 目標

200 * 200 の行列ベクトル積をできるだけ高速に動かせる実装を見つけ出すことを目指します。

200 とした理由として、 AtCoderにFP16の行列をbase64で埋め込むことを考えると、埋め込めるパラメータ数Nは 512 * 1024 >= 4 * ceil(N*2/3)
となり N <= 196608となります。

4層のNNを考えると、1つの行列のサイズは sqrt(199608/4) = 221となるため、　200くらいが妥当と考えました。

## ALU2024 Docker image builds

`src/ALU2024_Dockerfile` は、 AtCoder の言語アップデート用 TOML に含まれる `install` スクリプトをそのまま実行するための Dockerfile です。
以下のように指定することで、 `src/cpython/082-3-13_cpython.toml` から CPython 3.13.7 イメージを構築できます。

```
docker build -f src/ALU2024_Dockerfile \
  --build-arg INSTALL_TOML=src/cpython/082-3-13_cpython.toml \
  -t ac-cpython:3.13 .
```

`install` ブロックに含まれる `sudo` は Docker ビルド中に root で実行できるよう自動的に無効化されます。apt や pip を使うため、ビルドにはインターネット接続が必要です。

### TOML `install` スクリプトとの対応関係

`src/ALU2024_Dockerfile` は `ARG INSTALL_TOML` で指定した TOML を `/tmp/install.toml` としてコピーします。`RUN ... python3` のステップでは tomllib で `install` キーを読み出し、`sudo ` を文字列置換で外した上で `/tmp/install.sh` に保存します。その後の `RUN bash /tmp/install.sh` が AtCoder 側が公開しているインストール手順を丸ごと実行する部分に相当します。よって、TOML 内の `install` ブロックで記載されたコマンド列が、`sudo` 除去以外の改変なしで Docker レイヤー上に適用される構造になっています。
