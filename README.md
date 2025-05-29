README - Projeto Hello FastAPI Kubernetes com CI/CD e GitOps
Descrição

Este projeto demonstra como implementar um pipeline completo de CI/CD (Integração Contínua e Entrega Contínua) para uma aplicação FastAPI containerizada e implantada em um cluster Kubernetes, utilizando:

    Docker para containerização da aplicação

    Kubernetes (Kind) para orquestração de containers

    GitHub Actions para pipeline de build e push da imagem Docker

    ArgoCD para gerenciamento e entrega contínua (GitOps)

    Kustomize para gerenciamento de configurações Kubernetes

Estrutura do Projeto

.
├── .github/workflows/ci-cd.yml    # Workflow GitHub Actions para CI/CD
├── k8s/
│   ├── deployment.yaml            # Deployment Kubernetes
│   ├── service.yaml               # Service Kubernetes
│   ├── kustomization.yaml         # Configuração do Kustomize
│   └── pod.yaml                   # Pod simples (uso para testes)
├── app/                           # Código fonte da aplicação FastAPI
├── Dockerfile                     # Imagem Docker da aplicação
└── README.md

Como Funciona
1. Pipeline CI/CD no GitHub Actions

    Quando um código é enviado para o branch main, o workflow .github/workflows/ci-cd.yml é disparado.

    Ele realiza o checkout do código, autentica no Docker Hub usando segredos, constrói a imagem Docker e faz o push para o Docker Hub.

    Atualiza a tag da imagem no arquivo k8s/kustomization.yaml com o hash do commit para versionamento.

    Comita e faz push dessas alterações no repositório.

2. Gerenciamento da Infraestrutura com Kustomize

    O Kustomize permite customizar os manifests Kubernetes para usar a nova imagem com tag atualizada.

    O arquivo k8s/kustomization.yaml referencia deployment e service, além de atualizar a imagem.

3. Entrega Contínua com ArgoCD

    ArgoCD roda no cluster Kubernetes e monitora o repositório Git.

    Quando detecta mudança no branch principal, sincroniza o estado do cluster com a configuração declarada no Git.

    Isso cria/atualiza os recursos Kubernetes (deployment, service, etc) com a nova imagem.

Pré-requisitos

    Cluster Kubernetes (exemplo: Kind)

    Docker e conta no Docker Hub

    Conta no GitHub

    ArgoCD instalado no cluster (namespace argocd)

Passo a passo para rodar localmente

    Criar cluster Kind:

kind create cluster --name devops

Instalar ArgoCD:

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

Fazer login no ArgoCD:

kubectl port-forward svc/argocd-server -n argocd --address 0.0.0.0 8080:443

Acesse https://localhost:8080, usuário: admin

Obtenha senha:

kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d; echo

Configurar repositório GitHub:

    Criar repositório público/privado

    Criar segredos no GitHub: DOCKERHUB_USERNAME e DOCKERHUB_TOKEN

    Permitir permissão Read and write para GitHub Actions

Enviar código para GitHub

Criar aplicativo no ArgoCD:

    Application Name: hello-fastapi-k8s

    Project: default

    Sync Policy: Manual (ou Automatic)

    Repository URL: URL do seu repositório GitHub

    Revision: HEAD

    Path: k8s

    Cluster: https://kubernetes.default.svc

    Namespace: default

Sincronizar app no ArgoCD para implantar

Port-forward para acessar a aplicação:

    kubectl port-forward svc/hello-fastapi-service --address 0.0.0.0 8000:8000

    Acesse em http://localhost:8000

Arquivo de workflow (exemplo .github/workflows/ci-cd.yml)

name: CICD

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            seuusuario/hello-fastapi-k8s:latest
            seuusuario/hello-fastapi-k8s:${{ github.sha }}

      - name: Setup Kustomize
        uses: imranismail/setup-kustomize@v2

      - name: Update kustomization.yaml
        run: |
          cd k8s
          kustomize edit set image hello-fastapi=seuusuario/hello-fastapi-k8s:$GITHUB_SHA

      - name: Commit changes
        run: |
          git config --local user.name "GitHub Actions"
          git config --local user.email "actions@github.com"
          git commit -am "Update kustomization.yaml with new image"

      - name: Push changes
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ github.ref }}
