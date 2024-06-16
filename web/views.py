from django.shortcuts import render, get_object_or_404, redirect

from .models import Categoria, Producto, Cliente

from .carrito import Cart

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ClienteForm
from django.contrib.auth.decorators import login_required

# Create your views here.
""" VISTAS PARA EL CATALOGO DE PRODUCTOS """
def index(request):
    ListaProductos = Producto.objects.all()
    ListaCategoria = Categoria.objects.all()
    #print(ListaProductos)
    context = {
        'productos': ListaProductos,
        'categorias': ListaCategoria
    }
    return render(request, 'index.html', context)

def productosPorCategoria(request, categoria_id):
    """ Vista para filtrar productos por categoria """
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProductos = objCategoria.producto_set.all()

    listaCategorias = Categoria.objects.all()

    context = {
        'categorias': listaCategorias,
        'productos': listaProductos
    }

    return render(request, 'index.html', context)

def productosPorNombre(request):
    """ vista de filtrado de productos por nombre """
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__icontains=nombre)
    listaCategoria = Categoria.objects.all()

    context ={
        'categorias': listaCategoria,
        'productos': listaProductos
    }

    return render(request, 'index.html', context)

def productoDetalle(request, producto_id):
    """ Vista para mostrar el detalle de un producto """
    #objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto, pk=producto_id)

    context = {
        'producto': objProducto
    }

    return render(request, 'producto.html', context)

""" Vistas para el carrito de compras """

def carrito(request):
    return render(request, 'carrito.html')

def agregarCarrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1    

    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto, cantidad)

    #print(request.session['cart'])

    if request.method == 'GET':
        return redirect('/')

    return render(request, 'carrito.html')

def eliminarProductoCarrito(request,producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request, 'carrito.html')

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()

    return render(request, 'carrito.html')


""" Vistas para clientes y usuarios """

def crearUsuario(request):

    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        nuevoUsuario = User.objects.create_user(username=dataUsuario, password=dataPassword)
        if nuevoUsuario is not None:
            login(request, nuevoUsuario)
            return redirect('/cuenta')

    return render(request, 'login.html')

def loginUsuario(request):
    paginaDestino = request.GET.get('next', None)
    context = {
        'destino': paginaDestino,
    }

    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        usuarioAuth = authenticate(request ,username=dataUsuario, password=dataPassword)
        if usuarioAuth is not None:
            login(request, usuarioAuth)

            if dataDestino != 'None':
                return redirect(dataDestino)

            return redirect('/cuenta')
        
        else:
            context = {
                'mensajeError': 'Datos incorrectos'
            }

    return render(request, 'login.html', context)    

def logoutUsuario(request):
    logout(request)
    return render(request, 'login.html')


def cuentaUsuario(request):
    try:
        clienteEditar = Cliente.objects.get(usuario=request.user)

        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
            'cedula': clienteEditar.cedula,
            'direccion': clienteEditar.direccion,
            'telefono': clienteEditar.telefono,
            'sexo': clienteEditar.sexo,
            'fecha_nacimiento': clienteEditar.fecha_nacimiento
        }

        
    except:
        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email
        }    

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente': frmCliente
    } 

    return render(request, 'cuenta.html', context)

def actualizarCliente(request):
    mensaje = ""

    if request.method == 'POST':
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data

            #actualizar usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente['nombre']
            actUsuario.last_name = dataCliente['apellidos']
            actUsuario.email = dataCliente['email']
            actUsuario.save()

            #registar cliente
            nuevoCliente = Cliente()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.cedula = dataCliente['cedula']
            nuevoCliente.direccion = dataCliente['direccion']
            nuevoCliente.telefono = dataCliente['telefono']
            nuevoCliente.sexo = dataCliente['sexo']
            nuevoCliente.fecha_nacimiento = dataCliente['fecha_nacimiento']
            nuevoCliente.save()

            mensaje = "Datos actualizados correctamente"

    context = {
        'frmCliente': frmCliente,
        'mensaje': mensaje
    }        

    return render(request, 'cuenta.html',context)

""" Vistas para el proceso de compra """
@login_required(login_url='/login')
def registrarPedido(request):
    try:
        clienteEditar = Cliente.objects.get(usuario=request.user)

        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
            'cedula': clienteEditar.cedula,
            'direccion': clienteEditar.direccion,
            'telefono': clienteEditar.telefono,
            'sexo': clienteEditar.sexo,
            'fecha_nacimiento': clienteEditar.fecha_nacimiento
        }

        
    except:
        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email
        }    

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente': frmCliente
    } 

    return render(request, 'pedido.html', context)