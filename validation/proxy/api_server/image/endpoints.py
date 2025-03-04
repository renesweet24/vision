from core import Task
import fastapi
from fastapi.responses import JSONResponse
from models import base_models, synapses, utility_models, request_models
from validation.proxy import get_synapse, validation_utils
from fastapi import routing
from validation.proxy.api_server.image import utils
from validation.core_validator import core_validator

from validation.proxy import dependencies

router = routing.APIRouter(tags=["image"])


@router.post("/text-to-image")
async def text_to_image(
    body: request_models.TextToImageRequest,
    _: None = fastapi.Depends(dependencies.get_token),
) -> request_models.TextToImageResponse:
    synapse: synapses.TextToImage = get_synapse.get_synapse_from_body(
        body=body,
        synapse_model=synapses.TextToImage,
    )

    result: utility_models.QueryResult = await core_validator.make_organic_query(
        synapse=synapse,
        outgoing_model=base_models.TextToImageOutgoing,
        task=Task(synapse.engine + "-text-to-image"),
        stream=False,
    )
    if isinstance(result, JSONResponse):
        return result
    validation_utils.handle_bad_result(result)

    formatted_response: base_models.TextToImageOutgoing = result.formatted_response

    utils.do_formatted_response_image_checks(formatted_response, result)
    return request_models.TextToImageResponse(image_b64=formatted_response.image_b64)


@router.post("/image-to-image")
async def image_to_image(
    body: request_models.ImageToImageRequest,
    _: None = fastapi.Depends(dependencies.get_token),
) -> request_models.ImageToImageResponse:
    synapse: synapses.ImageToImage = get_synapse.get_synapse_from_body(
        body=body,
        synapse_model=synapses.ImageToImage,
    )

    result: utility_models.QueryResult = await core_validator.make_organic_query(
        synapse=synapse,
        outgoing_model=base_models.ImageToImageOutgoing,
        task=Task(synapse.engine + "-image-to-image"),
        stream=False,
    )
    if isinstance(result, JSONResponse):
        return result
    validation_utils.handle_bad_result(result)

    formatted_response: base_models.ImageToImageOutgoing = result.formatted_response

    utils.do_formatted_response_image_checks(formatted_response, result)
    return request_models.ImageToImageResponse(image_b64=formatted_response.image_b64)


@router.post("/inpaint")
async def inpaint(
    body: request_models.InpaintRequest,
    _: None = fastapi.Depends(dependencies.get_token),
) -> request_models.InpaintResponse:
    synapse = get_synapse.get_synapse_from_body(
        body=body,
        synapse_model=synapses.Inpaint,
    )

    result = await core_validator.make_organic_query(
        synapse=synapse, outgoing_model=base_models.InpaintOutgoing, task=Task("inpaint"), stream=False
    )
    if isinstance(result, JSONResponse):
        return result
    validation_utils.handle_bad_result(result)

    formatted_response: base_models.InpaintOutgoing = result.formatted_response

    utils.do_formatted_response_image_checks(formatted_response, result)

    return request_models.InpaintResponse(image_b64=formatted_response.image_b64)


@router.post("/avatar")
async def avatar(
    body: request_models.AvatarRequest,
    _: None = fastapi.Depends(dependencies.get_token),
) -> request_models.AvatarResponse:
    synapse = get_synapse.get_synapse_from_body(
        body=body,
        synapse_model=synapses.Avatar,
    )

    result = await core_validator.make_organic_query(
        synapse=synapse, outgoing_model=base_models.AvatarOutgoing, task=Task("avatar"), stream=False
    )
    if isinstance(result, JSONResponse):
        return result
    validation_utils.handle_bad_result(result)

    formatted_response: base_models.AvatarOutgoing = result.formatted_response

    utils.do_formatted_response_image_checks(formatted_response, result)

    return request_models.AvatarResponse(image_b64=formatted_response.image_b64)


# @router.post("/upscale")
# async def upscale(
#     body: request_models.UpscaleRequest,
#     _: None = fastapi.Depends(dependencies.get_token),
# ) -> request_models.UpscaleResponse:
#     synapse = get_synapse.get_synapse_from_body(
#         body=body,
#         synapse_model=synapses.Upscale,
#     )

#     result = await core_validator.make_organic_query(
#         synapse=synapse, outgoing_model=base_models.UpscaleOutgoing, task=Task("upscale"), stream=False
#     )
#     if isinstance(result, JSONResponse):
#         return result
#     validation_utils.handle_bad_result(result)

#     formatted_response: base_models.UpscaleOutgoing = result.formatted_response

#     utils.do_formatted_response_image_checks(formatted_response, result)

#     return request_models.UpscaleResponse(image_b64=formatted_response.image_b64)


# @router.post("/clip-embeddings")
# async def clip_embeddings(
#     body: request_models.ClipEmbeddingsRequest,
#     _: None = fastapi.Depends(dependencies.get_token),
# ) -> request_models.ClipEmbeddingsResponse:
#     altered_clip_body = validation_utils.alter_clip_body(body)
#     synapse = get_synapse.get_synapse_from_body(
#         body=altered_clip_body,
#         synapse_model=synapses.ClipEmbeddings,
#     )

#     result = await core_validator.make_organic_query(
#         synapse=synapse,
#         outgoing_model=base_models.ClipEmbeddingsOutgoing,
#         task=Task("clip-image-embeddings"),
#         stream=False,
#     )
#     if isinstance(result, JSONResponse):
#         return result
#     if result is None:
#         raise HTTPException(
#             status_code=fastapi.status.HTTP_400_BAD_REQUEST,
#             detail="I'm sorry, no valid response was possible from the miners :/",
#         )

#     formatted_response: base_models.ClipEmbeddingsOutgoing = result.formatted_response

#     return request_models.ClipEmbeddingsResponse(
#         clip_embeddings=formatted_response.clip_embeddings,
#     )
