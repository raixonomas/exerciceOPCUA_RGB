import asyncio

from asyncua import Server, ua
from random import randint

async def main():
    server = Server()
    await server.init()
    server.set_server_name("OPC UA SERVER DEMO")

    url = "opc.tcp://10.4.1.218:4840"
    server.set_endpoint(url)
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity,
                                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                                ua.SecurityPolicyType.Basic256Sha256_Sign])
    name = "OPC_UA_SERVER"
    namespace = await server.register_namespace(name)

    motor = await server.nodes.objects.add_object(namespace, "motor_1")

    node_blue = await motor.add_variable(namespace, "Blue", False)
    node_red = await motor.add_variable(namespace, "Red", False)
    node_green = await motor.add_variable(namespace, "Green", True)

    await node_blue.set_writable(True)
    await node_red.set_writable(True)
    await node_green.set_writable(True)

    async with server:
        while True:
            does_open_red = randint(0, 1)
            if(does_open_red == 1):
                await node_red.set_value(True)
            else:
                await node_red.set_value(False)

            does_open_blue = randint(0, 1)
            if (does_open_blue == 1):
                await node_blue.set_value(True)
            else:
                await node_blue.set_value(False)

            does_open_green = randint(0, 1)
            if (does_open_green == 1):
                await node_green.set_value(True)
            else:
                await node_green.set_value(False)

            await asyncio.sleep(0.1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Fin")
