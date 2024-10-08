"""
Script to extract observations from low-dimensional simulation states in a robosuite dataset.

Args:
    dataset (str): path to input hdf5 dataset

    output_name (str): name of output hdf5 dataset

    n (int): if provided, stop after n trajectories are processed

    shaped (bool): if flag is set, use dense rewards

    camera_names (str or [str]): camera name(s) to use for image observations. 
        Leave out to not use image observations.

    camera_height (int): height of image observation.

    camera_width (int): width of image observation

    done_mode (int): how to write done signal. If 0, done is 1 whenever s' is a success state.
        If 1, done is 1 at the end of each trajectory. If 2, both.

    copy_rewards (bool): if provided, copy rewards from source file instead of inferring them

    copy_dones (bool): if provided, copy dones from source file instead of inferring them

Example usage:
    
    # extract low-dimensional observations
    python dataset_states_to_obs.py --dataset /path/to/demo.hdf5 --output_name low_dim.hdf5 --done_mode 2
    
    # extract 84x84 image observations
    python dataset_states_to_obs.py --dataset /path/to/demo.hdf5 --output_name image.hdf5 \
        --done_mode 2 --camera_names agentview robot0_eye_in_hand --camera_height 84 --camera_width 84

    # extract 84x84 image and depth observations
    python dataset_states_to_obs.py --dataset /path/to/demo.hdf5 --output_name depth.hdf5 \
        --done_mode 2 --camera_names agentview robot0_eye_in_hand --camera_height 84 --camera_width 84 --depth

    # (space saving option) extract 84x84 image observations with compression and without 
    # extracting next obs (not needed for pure imitation learning algos)
    python dataset_states_to_obs.py --dataset /path/to/demo.hdf5 --output_name image.hdf5 \
        --done_mode 2 --camera_names agentview robot0_eye_in_hand --camera_height 84 --camera_width 84 \
        --compress --exclude-next-obs

    # use dense rewards, and only annotate the end of trajectories with done signal
    python dataset_states_to_obs.py --dataset /path/to/demo.hdf5 --output_name image_dense_done_1.hdf5 \
        --done_mode 1 --dense --camera_names agentview robot0_eye_in_hand --camera_height 84 --camera_width 84


    python dataset_states_to_obs.py --dataset  /home/lawchen/project/robomimic/datasets/lift/ph/demo_v141.hdf5 --output_name image_v141_100cams_curriculum.hdf5 \
    --done_mode 2 --camera_names agentview birdview frontview sideview robot0_eye_in_hand agentview_0 agentview_1 agentview_2 agentview_3 agentview_4 agentview_5 agentview_6 \
    agentview_7 agentview_8 agentview_9 agentview_10 agentview_11 agentview_12 agentview_13 agentview_14 agentview_15 agentview_16 \
    agentview_17 agentview_18 agentview_19 agentview_20 agentview_21 agentview_22 agentview_23 agentview_24 agentview_25 agentview_26 \
    agentview_27 agentview_28 agentview_29 agentview_30 agentview_31 agentview_32 agentview_33 agentview_34 agentview_35 agentview_36 \
        agentview_37 agentview_38 agentview_39 agentview_40 agentview_41 agentview_42 agentview_43 agentview_44 agentview_45 agentview_46 \
            agentview_47 agentview_48 agentview_49 agentview_50 agentview_51 agentview_52 agentview_53 agentview_54 agentview_55 agentview_56 \
                agentview_57 agentview_58 agentview_59 agentview_60 agentview_61 agentview_62 agentview_63 agentview_64 agentview_65 agentview_66 \
                    agentview_67 agentview_68 agentview_69 agentview_70 agentview_71 agentview_72 agentview_73 agentview_74 agentview_75 agentview_76 \
                        agentview_77 agentview_78 agentview_79 agentview_80 agentview_81 agentview_82 agentview_83 agentview_84 agentview_85 \
                            agentview_86 agentview_87 agentview_88 agentview_89 agentview_90 agentview_91 agentview_92 agentview_93 agentview_94 \
                                agentview_95 agentview_96 agentview_97 agentview_98 agentview_99 agentview_100 \
                                    --camera_height 84 --camera_width 84 --exclude_next_obs
    
    python dataset_states_to_obs.py --dataset  /home/lawchen/project/robomimic/datasets/lift/ph/demo_v141.hdf5 --output_name image_v141_500cams.hdf5 \
    --done_mode 2 --camera_names agentview birdview frontview sideview robot0_eye_in_hand agentview_1 agentview_2 agentview_3 agentview_4 agentview_5 agentview_6 \
    agentview_7 agentview_8 agentview_9 agentview_10 agentview_11 agentview_12 agentview_13 agentview_14 agentview_15 agentview_16 \
    agentview_17 agentview_18 agentview_19 agentview_20 agentview_21 agentview_22 agentview_23 agentview_24 agentview_25 agentview_26 \
    agentview_27 agentview_28 agentview_29 agentview_30 agentview_31 agentview_32 agentview_33 agentview_34 agentview_35 agentview_36 \
        agentview_37 agentview_38 agentview_39 agentview_40 agentview_41 agentview_42 agentview_43 agentview_44 agentview_45 agentview_46 \
            agentview_47 agentview_48 agentview_49 agentview_50 agentview_51 agentview_52 agentview_53 agentview_54 agentview_55 agentview_56 \
                agentview_57 agentview_58 agentview_59 agentview_60 agentview_61 agentview_62 agentview_63 agentview_64 agentview_65 agentview_66 \
                    agentview_67 agentview_68 agentview_69 agentview_70 agentview_71 agentview_72 agentview_73 agentview_74 agentview_75 agentview_76 \
                        agentview_77 agentview_78 agentview_79 agentview_80 agentview_81 agentview_82 agentview_83 agentview_84 agentview_85 \
                            agentview_86 agentview_87 agentview_88 agentview_89 agentview_90 agentview_91 agentview_92 agentview_93 agentview_94 \
                                agentview_95 agentview_96 agentview_97 agentview_98 agentview_99 agentview_100 \
        agentview_101 agentview_102 agentview_103 agentview_104 agentview_105 agentview_106 agentview_107 agentview_108 agentview_109 agentview_110 \
            agentview_111 agentview_112 agentview_113 agentview_114 agentview_115 agentview_116 agentview_117 agentview_118 agentview_119 agentview_120 \
                agentview_121 agentview_122 agentview_123 agentview_124 agentview_125 agentview_126 agentview_127 agentview_128 agentview_129 agentview_130 \
                    agentview_131 agentview_132 agentview_133 agentview_134 agentview_135 agentview_136 agentview_137 agentview_138 agentview_139 agentview_140 \
                        agentview_141 agentview_142 agentview_143 agentview_144 agentview_145 agentview_146 agentview_147 agentview_148 agentview_149 agentview_150 \
                            agentview_151 agentview_152 agentview_153 agentview_154 agentview_155 agentview_156 agentview_157 agentview_158 agentview_159 agentview_160 \
                                agentview_161 agentview_162 agentview_163 agentview_164 agentview_165 agentview_166 agentview_167 agentview_168 agentview_169 agentview_170 \
                                    agentview_171 agentview_172 agentview_173 agentview_174 agentview_175 agentview_176 agentview_177 agentview_178 agentview_179 agentview_180 \
                                        agentview_181 agentview_182 agentview_183 agentview_184 agentview_185 agentview_186 agentview_187 agentview_188 agentview_189 agentview_190 \
                                            agentview_191 agentview_192 agentview_193 agentview_194 agentview_195 agentview_196 agentview_197 agentview_198 agentview_199 agentview_200 \
        agentview_201 agentview_202 agentview_203 agentview_204 agentview_205 agentview_206 agentview_207 agentview_208 agentview_209 agentview_210 \
            agentview_211 agentview_212 agentview_213 agentview_214 agentview_215 agentview_216 agentview_217 agentview_218 agentview_219 agentview_220 \
                agentview_221 agentview_222 agentview_223 agentview_224 agentview_225 agentview_226 agentview_227 agentview_228 agentview_229 agentview_230 \
                    agentview_231 agentview_232 agentview_233 agentview_234 agentview_235 agentview_236 agentview_237 agentview_238 agentview_239 agentview_240 \
                        agentview_241 agentview_242 agentview_243 agentview_244 agentview_245 agentview_246 agentview_247 agentview_248 agentview_249 agentview_250 \
                            agentview_251 agentview_252 agentview_253 agentview_254 agentview_255 agentview_256 agentview_257 agentview_258 agentview_259 agentview_260 \
                                agentview_261 agentview_262 agentview_263 agentview_264 agentview_265 agentview_266 agentview_267 agentview_268 agentview_269 agentview_270 \
                                    agentview_271 agentview_272 agentview_273 agentview_274 agentview_275 agentview_276 agentview_277 agentview_278 agentview_279 agentview_280 \
                                        agentview_281 agentview_282 agentview_283 agentview_284 agentview_285 agentview_286 agentview_287 agentview_288 agentview_289 agentview_290 \
                                            agentview_291 agentview_292 agentview_293 agentview_294 agentview_295 agentview_296 agentview_297 agentview_298 agentview_299 agentview_300 \
        agentview_301 agentview_302 agentview_303 agentview_304 agentview_305 agentview_306 agentview_307 agentview_308 agentview_309 agentview_310 \
            agentview_311 agentview_312 agentview_313 agentview_314 agentview_315 agentview_316 agentview_317 agentview_318 agentview_319 agentview_320 \
                agentview_321 agentview_322 agentview_323 agentview_324 agentview_325 agentview_326 agentview_327 agentview_328 agentview_329 agentview_330 \
                    agentview_331 agentview_332 agentview_333 agentview_334 agentview_335 agentview_336 agentview_337 agentview_338 agentview_339 agentview_340 \
                        agentview_341 agentview_342 agentview_343 agentview_344 agentview_345 agentview_346 agentview_347 agentview_348 agentview_349 agentview_350 \
                            agentview_351 agentview_352 agentview_353 agentview_354 agentview_355 agentview_356 agentview_357 agentview_358 agentview_359 agentview_360 \
                                agentview_361 agentview_362 agentview_363 agentview_364 agentview_365 agentview_366 agentview_367 agentview_368 agentview_369 agentview_370 \
                                    agentview_371 agentview_372 agentview_373 agentview_374 agentview_375 agentview_376 agentview_377 agentview_378 agentview_379 agentview_380 \
                                        agentview_381 agentview_382 agentview_383 agentview_384 agentview_385 agentview_386 agentview_387 agentview_388 agentview_389 agentview_390 \
                                            agentview_391 agentview_392 agentview_393 agentview_394 agentview_395 agentview_396 agentview_397 agentview_398 agentview_399 agentview_400 \
                                                agentview_401 agentview_402 agentview_403 agentview_404 agentview_405 agentview_406 agentview_407 agentview_408 agentview_409 agentview_410 \
        agentview_411 agentview_412 agentview_413 agentview_414 agentview_415 agentview_416 agentview_417 agentview_418 agentview_419 agentview_420 \
            agentview_421 agentview_422 agentview_423 agentview_424 agentview_425 agentview_426 agentview_427 agentview_428 agentview_429 agentview_430 \
                agentview_431 agentview_432 agentview_433 agentview_434 agentview_435 agentview_436 agentview_437 agentview_438 agentview_439 agentview_440 \
                    agentview_441 agentview_442 agentview_443 agentview_444 agentview_445 agentview_446 agentview_447 agentview_448 agentview_449 agentview_450 \
                        agentview_451 agentview_452 agentview_453 agentview_454 agentview_455 agentview_456 agentview_457 agentview_458 agentview_459 agentview_460 \
                            agentview_461 agentview_462 agentview_463 agentview_464 agentview_465 agentview_466 agentview_467 agentview_468 agentview_469 agentview_470 \
                                agentview_471 agentview_472 agentview_473 agentview_474 agentview_475 agentview_476 agentview_477 agentview_478 agentview_479 agentview_480 \
                                    agentview_481 agentview_482 agentview_483 agentview_484 agentview_485 agentview_486 agentview_487 agentview_488 agentview_489 agentview_490 \
                                        agentview_491 agentview_492 agentview_493 agentview_494 agentview_495 agentview_496 agentview_497 agentview_498 agentview_499 agentview_500
                                    --camera_height 84 --camera_width 84
"""
import os
import json
import h5py
import argparse
import numpy as np
from copy import deepcopy
from tqdm import tqdm

import robomimic.utils.tensor_utils as TensorUtils
import robomimic.utils.file_utils as FileUtils
import robomimic.utils.env_utils as EnvUtils
from robomimic.envs.env_base import EnvBase


def extract_trajectory(
    env, 
    initial_state, 
    states, 
    actions,
    done_mode,
    camera_names=None, 
    camera_height=84, 
    camera_width=84,
):
    """
    Helper function to extract observations, rewards, and dones along a trajectory using
    the simulator environment.

    Args:
        env (instance of EnvBase): environment
        initial_state (dict): initial simulation state to load
        states (np.array): array of simulation states to load to extract information
        actions (np.array): array of actions
        done_mode (int): how to write done signal. If 0, done is 1 whenever s' is a 
            success state. If 1, done is 1 at the end of each trajectory. 
            If 2, do both.
    """
    assert isinstance(env, EnvBase)
    assert states.shape[0] == actions.shape[0]
    # breakpoint()
    # load the initial state
    env.reset()
    obs, camera_info = env.reset_to(initial_state)

    # maybe add in intrinsics and extrinsics for all cameras
    # camera_info = None
    # is_robosuite_env = EnvUtils.is_robosuite_env(env=env)
    # if is_robosuite_env:
    #     camera_info = get_camera_info(
    #         env=env,
    #         camera_names=camera_names, 
    #         camera_height=camera_height, 
    #         camera_width=camera_width,
    #     )

    traj = dict(
        obs=[], 
        next_obs=[], 
        rewards=[], 
        dones=[], 
        actions=np.array(actions), 
        states=np.array(states), 
        initial_state_dict=initial_state,
        camera_info=dict(),
    )
    for cam_name in camera_info.keys():
        traj["camera_info"][cam_name] = {"intrinsics": [], "extrinsics": []} # "pose": [], 

    traj_len = states.shape[0]
    # iteration variable @t is over "next obs" indices
    for t in range(1, traj_len + 1):

        # get next observation
        if t == traj_len:
            # play final action to get next observation for last timestep
            next_obs, _, _, _ = env.step(actions[t - 1])
        else:
            # reset to simulator state to get observation
            # breakpoint()
            next_obs, next_camera_info = env.reset_to({"states" : states[t]}) # robomimic/robomimic/envs/env_robosuite.py:L135

        # infer reward signal
        # note: our tasks use reward r(s'), reward AFTER transition, so this is
        #       the reward for the current timestep
        r = env.get_reward()

        # infer done signal
        done = False
        if (done_mode == 1) or (done_mode == 2):
            # done = 1 at end of trajectory
            done = done or (t == traj_len)
        if (done_mode == 0) or (done_mode == 2):
            # done = 1 when s' is task success state
            done = done or env.is_success()["task"]
        done = int(done)

        # collect transition
        traj["obs"].append(obs)
        # update traj["camera_info"]
        for cam_name in traj["camera_info"]:
            traj["camera_info"][cam_name]["intrinsics"].append(camera_info[cam_name]["camera_intrinsics"])
            # traj["camera_info"][cam_name]["pose"].append(camera_info[cam_name]["camera_pose"])
            traj["camera_info"][cam_name]["extrinsics"].append(camera_info[cam_name]["camera_extrinsics"])

        traj["next_obs"].append(next_obs)
        traj["rewards"].append(r)
        traj["dones"].append(done)

        # update for next iter
        obs = deepcopy(next_obs)
        camera_info = deepcopy(next_camera_info)

    # convert list of dict to dict of list for obs dictionaries (for convenient writes to hdf5 dataset)
    traj["obs"] = TensorUtils.list_of_flat_dict_to_dict_of_list(traj["obs"])
    traj["next_obs"] = TensorUtils.list_of_flat_dict_to_dict_of_list(traj["next_obs"])

    # list to numpy array
    for k in traj:
        if k == "initial_state_dict" or k == "camera_info":
            continue
        if isinstance(traj[k], dict):
            for kp in traj[k]:
                traj[k][kp] = np.array(traj[k][kp])
        else:
            traj[k] = np.array(traj[k])

    return traj, camera_info


def get_camera_info(
    env,
    camera_names=None, 
    camera_height=84, 
    camera_width=84,
):
    """
    Helper function to get camera intrinsics and extrinsics for cameras being used for observations.
    """

    # TODO: make this function more general than just robosuite environments
    assert EnvUtils.is_robosuite_env(env=env)

    if camera_names is None:
        return None

    camera_info = dict()
    for cam_name in camera_names:
        K = env.get_camera_intrinsic_matrix(camera_name=cam_name, camera_height=camera_height, camera_width=camera_width)
        R = env.get_camera_extrinsic_matrix(camera_name=cam_name) # camera pose in world frame
        if "eye_in_hand" in cam_name:
            # convert extrinsic matrix to be relative to robot eef control frame
            assert cam_name.startswith("robot0")
            eef_site_name = env.base_env.robots[0].controller.eef_name
            eef_pos = np.array(env.base_env.sim.data.site_xpos[env.base_env.sim.model.site_name2id(eef_site_name)])
            eef_rot = np.array(env.base_env.sim.data.site_xmat[env.base_env.sim.model.site_name2id(eef_site_name)].reshape([3, 3]))
            eef_pose = np.zeros((4, 4)) # eef pose in world frame
            eef_pose[:3, :3] = eef_rot
            eef_pose[:3, 3] = eef_pos
            eef_pose[3, 3] = 1.0
            eef_pose_inv = np.zeros((4, 4))
            eef_pose_inv[:3, :3] = eef_pose[:3, :3].T
            eef_pose_inv[:3, 3] = -eef_pose_inv[:3, :3].dot(eef_pose[:3, 3])
            eef_pose_inv[3, 3] = 1.0
            R = R.dot(eef_pose_inv) # T_E^W * T_W^C = T_E^C
        camera_info[cam_name] = dict(
            intrinsics=K.tolist(),
            extrinsics=R.tolist(),
        )
    return camera_info

from robosuite.wrappers import DomainRandomizationWrapper
import robosuite.macros as macros
# We'll use instance randomization so that entire geom groups are randomized together
macros.USING_INSTANCE_RANDOMIZATION = True


def dataset_states_to_obs(args):
    if args.depth:
        assert len(args.camera_names) > 0, "must specify camera names if using depth"

    # create environment to use for data processing
    env_meta = FileUtils.get_env_metadata_from_dataset(dataset_path=args.dataset)
    env = EnvUtils.create_env_for_data_processing(
        env_meta=env_meta,
        camera_names=args.camera_names, 
        camera_height=args.camera_height, 
        camera_width=args.camera_width, 
        reward_shaping=args.shaped,
        use_depth_obs=args.depth,
    )


    env.env = DomainRandomizationWrapper(env.env, randomize_color=False, 
                                     randomize_camera=True, 
                                     randomize_lighting=True,
                                     camera_randomization_args={'camera_names': [x for x in env.env.sim.model.camera_names if x != "robot0_eye_in_hand"], 
                                                                'fovy_perturbation_size': 15.0, 
                                                                'position_perturbation_size': 0.05, 
                                                                'randomize_fovy': True, 
                                                                'randomize_position': True, 
                                                                'randomize_rotation': True, 
                                                                'rotation_perturbation_size': 0.07}, 
                                     lighting_randomization_args={'ambient_perturbation_size': 0.1, 
                                                                  'diffuse_perturbation_size': 0.1, 
                                                                  'direction_perturbation_size':1, 
                                                                  'light_names': None, 
                                                                  'position_perturbation_size': 1, 
                                                                  'randomize_active': False, 
                                                                  'randomize_ambient': False, 
                                                                  'randomize_diffuse': False, 
                                                                  'randomize_direction': True, 
                                                                  'randomize_position': True, 
                                                                  'randomize_specular': True, 
                                                                  'specular_perturbation_size': 0.8}
    )


    print("==== Using environment with the following metadata ====")
    print(json.dumps(env.serialize(), indent=4))
    print("")

    # some operations for playback are robosuite-specific, so determine if this environment is a robosuite env
    is_robosuite_env = EnvUtils.is_robosuite_env(env_meta)

    # list of all demonstration episodes (sorted in increasing number order)
    f = h5py.File(args.dataset, "r")
    demos = list(f["data"].keys())
    inds = np.argsort([int(elem[5:]) for elem in demos])
    demos = [demos[i] for i in inds]

    # maybe reduce the number of demonstrations to playback
    if args.n is not None:
        demos = demos[:args.n]

    # output file in same directory as input file
    output_path = os.path.join(os.path.dirname(args.dataset), args.output_name)
    f_out = h5py.File(output_path, "w")
    data_grp = f_out.create_group("data")
    print("input file: {}".format(args.dataset))
    print("output file: {}".format(output_path))

    total_samples = 0
    for ind in tqdm(range(len(demos))):
        ep = demos[ind]

        # prepare initial state to reload from
        states = f["data/{}/states".format(ep)][()]
        initial_state = dict(states=states[0])
        if is_robosuite_env:
            initial_state["model"] = f["data/{}".format(ep)].attrs["model_file"]

        # extract obs, rewards, dones
        actions = f["data/{}/actions".format(ep)][()]
        traj, camera_info = extract_trajectory(
            env=env, 
            initial_state=initial_state, 
            states=states, 
            actions=actions,
            done_mode=args.done_mode,
            camera_names=args.camera_names, 
            camera_height=args.camera_height, 
            camera_width=args.camera_width,
        )

        # maybe copy reward or done signal from source file
        if args.copy_rewards:
            traj["rewards"] = f["data/{}/rewards".format(ep)][()]
        if args.copy_dones:
            traj["dones"] = f["data/{}/dones".format(ep)][()]

        # store transitions

        # IMPORTANT: keep name of group the same as source file, to make sure that filter keys are
        #            consistent as well
        ep_data_grp = data_grp.create_group(ep)
        ep_data_grp.create_dataset("actions", data=np.array(traj["actions"]))
        ep_data_grp.create_dataset("states", data=np.array(traj["states"]))
        ep_data_grp.create_dataset("rewards", data=np.array(traj["rewards"]))
        ep_data_grp.create_dataset("dones", data=np.array(traj["dones"]))
        for k in traj["obs"]:
            if args.compress:
                ep_data_grp.create_dataset("obs/{}".format(k), data=np.array(traj["obs"][k]), compression="gzip")
            else:
                ep_data_grp.create_dataset("obs/{}".format(k), data=np.array(traj["obs"][k]))
            if not args.exclude_next_obs:
                if args.compress:
                    ep_data_grp.create_dataset("next_obs/{}".format(k), data=np.array(traj["next_obs"][k]), compression="gzip")
                else:
                    ep_data_grp.create_dataset("next_obs/{}".format(k), data=np.array(traj["next_obs"][k]))

        cam_info_group_all = ep_data_grp.create_group("camera_info")
        for cam in traj["camera_info"].keys():
            cam_info_group = cam_info_group_all.create_group(f"{cam}")
            for k in traj["camera_info"][cam].keys():
                cam_info_group.create_dataset(f"{k}", data=traj["camera_info"][cam][k])

        # episode metadata
        if is_robosuite_env:
            ep_data_grp.attrs["model_file"] = traj["initial_state_dict"]["model"] # model xml for this episode
        ep_data_grp.attrs["num_samples"] = traj["actions"].shape[0] # number of transitions in this episode

        if camera_info is not None:
            assert is_robosuite_env
            ep_data_grp.attrs["camera_info"] = json.dumps(camera_info, indent=4)

        total_samples += traj["actions"].shape[0]


    # copy over all filter keys that exist in the original hdf5
    if "mask" in f:
        f.copy("mask", f_out)

    # global metadata
    data_grp.attrs["total"] = total_samples
    data_grp.attrs["env_args"] = json.dumps(env.serialize(), indent=4) # environment info
    print("Wrote {} trajectories to {}".format(len(demos), output_path))

    f.close()
    f_out.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="path to input hdf5 dataset",
    )
    # name of hdf5 to write - it will be in the same directory as @dataset
    parser.add_argument(
        "--output_name",
        type=str,
        required=True,
        help="name of output hdf5 dataset",
    )

    # specify number of demos to process - useful for debugging conversion with a handful
    # of trajectories
    parser.add_argument(
        "--n",
        type=int,
        default=None,
        help="(optional) stop after n trajectories are processed",
    )

    # flag for reward shaping
    parser.add_argument(
        "--shaped", 
        action='store_true',
        help="(optional) use shaped rewards",
    )

    # camera names to use for observations
    parser.add_argument(
        "--camera_names",
        type=str,
        nargs='+',
        default=[],
        help="(optional) camera name(s) to use for image observations. Leave out to not use image observations.",
    )

    parser.add_argument(
        "--camera_height",
        type=int,
        default=84,
        help="(optional) height of image observations",
    )

    parser.add_argument(
        "--camera_width",
        type=int,
        default=84,
        help="(optional) width of image observations",
    )

    # flag for including depth observations per camera
    parser.add_argument(
        "--depth", 
        action='store_true',
        help="(optional) use depth observations for each camera",
    )

    # specifies how the "done" signal is written. If "0", then the "done" signal is 1 wherever 
    # the transition (s, a, s') has s' in a task completion state. If "1", the "done" signal 
    # is one at the end of every trajectory. If "2", the "done" signal is 1 at task completion
    # states for successful trajectories and 1 at the end of all trajectories.
    parser.add_argument(
        "--done_mode",
        type=int,
        default=0,
        help="how to write done signal. If 0, done is 1 whenever s' is a success state.\
            If 1, done is 1 at the end of each trajectory. If 2, both.",
    )

    # flag for copying rewards from source file instead of re-writing them
    parser.add_argument(
        "--copy_rewards", 
        action='store_true',
        help="(optional) copy rewards from source file instead of inferring them",
    )

    # flag for copying dones from source file instead of re-writing them
    parser.add_argument(
        "--copy_dones", 
        action='store_true',
        help="(optional) copy dones from source file instead of inferring them",
    )

    # flag to exclude next obs in dataset
    parser.add_argument(
        "--exclude-next-obs", 
        action='store_true',
        help="(optional) exclude next obs in dataset",
    )

    # flag to compress observations with gzip option in hdf5
    parser.add_argument(
        "--compress", 
        action='store_true',
        help="(optional) compress observations with gzip option in hdf5",
    )

    # exclude_next_obs
    parser.add_argument(
        "--exclude_next_obs",
        action='store_true',
        help="(optional) exclude next obs in dataset",
    )

    args = parser.parse_args()
    dataset_states_to_obs(args)
